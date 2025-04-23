from django.shortcuts import render
from .models import Product
from app_orders.models import Cart, CartItem


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/products.html', {'products': products})


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    in_cart = False

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        in_cart = CartItem.objects.filter(cart=cart, product=product).exists()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'in_cart': in_cart
    })
