from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Order
from app_products.models import Product
from .forms import OrderStatusUpdateForm


@require_POST
@csrf_exempt
def toggle_cart_item(request):
    data = json.loads(request.body)
    product_id = data.get("product_id")
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({"success": False, "message": "Вы не авторизованы."})

    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.get_or_create(user=user)

    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if cart_item:
        cart_item.delete()
        return JsonResponse({"success": True, "in_cart": False})
    else:
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        return JsonResponse({"success": True, "in_cart": True})


@require_POST
def cart_remove(request):
    item_id = request.POST.get('item_id')
    try:
        item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart = item.cart
        item.delete()
        items = cart.items.all()
        total_price = sum(i.quantity * i.product.price for i in items)
        return JsonResponse({'success': True, 'total_price': total_price})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in items)

    return render(request, 'orders/cart.html', {
        'cart': cart,
        'items': items,
        'total_price': total_price,
    })


@require_POST
def cart_update_quantity(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')

    try:
        item = CartItem.objects.select_related('product', 'cart').get(id=item_id, cart__user=request.user)

        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease':
            item.quantity -= 1

        if item.quantity <= 0:
            item.delete()
            quantity = 0
            subtotal = 0
        else:
            item.save()
            quantity = item.quantity
            subtotal = item.quantity * item.product.price

        total_price = sum(
            ci.quantity * ci.product.price
            for ci in CartItem.objects.filter(cart__user=request.user)
        )
        return JsonResponse({
            'success': True,
            'quantity': quantity,
            'subtotal': f"{subtotal:.2f}",
            'total_price': f"{total_price:.2f}"
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'})


def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order-detail', order_id=order_id)  # правильно
    else:
        form = OrderStatusUpdateForm(instance=order)

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'form': form
    })
