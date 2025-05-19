from django.shortcuts import render, get_object_or_404, redirect
from .models import Shop
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ShopCreationRequestForm
import os
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST


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


@require_POST
@login_required
def toggle_shop_status(request, slug):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        data = json.loads(request.body)
        shop = Shop.objects.get(slug=slug, owner=request.user)
        shop.is_active = data['is_active']
        shop.save()
        return JsonResponse({'success': True, 'is_active': shop.is_active})
    except Shop.DoesNotExist:
        return JsonResponse({'error': 'Shop not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def shop_create_request(request):
    if request.method == 'POST':
        form = ShopCreationRequestForm(request.POST, request.FILES)
        if form.is_valid():
            shop_request = form.save(commit=False)
            shop_request.user = request.user
            shop_request.save()
            return redirect('my-shops')
    else:
        form = ShopCreationRequestForm()

    return render(request, 'shops/shop_create_request.html', {'form': form})


@login_required
def shop_delete(request, slug):
    shop = get_object_or_404(Shop, slug=slug)

    if shop.owner != request.user:
        return redirect('my-shops')

    if request.method == 'POST':
        if shop.logo:
            logo_path = shop.logo.path
            if os.path.isfile(logo_path):
                os.remove(logo_path)

        shop.delete()
        return redirect('my-shops')

    shops = Shop.objects.all()
    return render(request, 'shops/shops.html', {'shops': shops})
