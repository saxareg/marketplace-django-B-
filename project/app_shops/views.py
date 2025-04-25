from django.shortcuts import render, get_object_or_404
from .models import Shop


def my_shops_view(request):
    shops = Shop.objects.filter(owner=request.user)
    return render(request, 'shops/shops.html', {'shops': shops})


def my_shop_detail(request, slug):
    shop = get_object_or_404(Shop, slug=slug)
    products = shop.products.all()  # related_name='products' в ForeignKey
    return render(request, 'shops/shop_detail.html', {
        'shop': shop,
        'products': products
    })
