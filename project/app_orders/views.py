from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from .models import Cart, CartItem
from app_products.models import Product


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
