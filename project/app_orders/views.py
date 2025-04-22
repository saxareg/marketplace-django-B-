from django.http import JsonResponse
from django.views.decorators.http import require_POST
from app_products.models import Product
from .models import Cart, CartItem


@require_POST
def add_to_cart_ajax(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    if not product_id:
        return JsonResponse({'error': 'Нет ID товара'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Товар не найден'}, status=404)

    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    item.quantity += quantity
    item.save()

    return JsonResponse({'success': True, 'message': 'Товар добавлен в корзину'})
