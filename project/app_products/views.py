from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review
from app_orders.models import Cart, CartItem, OrderItem
from app_shops.models import Shop
from .forms import ProductForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator


def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(slug__icontains=query) |
            Q(category__name__icontains=query) |
            Q(shop__name__icontains=query)
        ).distinct()

    paginator = Paginator(products, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/products.html', {
        'page_obj': page_obj,
        'query': query,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    in_cart = False
    is_owner = product.shop.owner == request.user
    can_review = False
    review_form = None

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        in_cart = CartItem.objects.filter(cart=cart, product=product).exists()

        has_paid = OrderItem.objects.filter(
            order__user=request.user,
            order__is_paid=True,
            product=product
        ).exists()

        has_reviewed = Review.objects.filter(user=request.user, product=product).exists()
        can_review = has_paid and not has_reviewed

        if can_review:
            review_form = ReviewForm()

    reviews = product.reviews.all().order_by('-created_at')

    return render(request, 'products/product_detail.html', {
        'product': product,
        'in_cart': in_cart,
        'is_owner': is_owner,
        'reviews': reviews,
        'can_review': can_review,
        'review_form': review_form,
    })


@login_required
def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if product.shop.owner != request.user:
        return redirect('product_detail', slug=slug)

    if request.method == 'POST':
        product.delete()
        shop_slug = product.shop.slug
        return redirect('shop-detail', slug=shop_slug)

    return redirect('product_detail', slug=slug)


@login_required()
def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if product.shop.owner != request.user:
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop-detail', slug=product.shop.slug)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_edit.html', {'form': form, 'product': product})


@login_required
def create_product(request):
    shop_slug = request.GET.get('shop')
    shop = get_object_or_404(Shop, slug=shop_slug)

    if shop.owner != request.user:
        return redirect('shop-detail', slug=shop.slug)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.save()
            return redirect('shop-detail', slug=shop.slug)
    else:
        form = ProductForm()

    return render(request, 'products/product_create.html', {'form': form, 'shop': shop})


@login_required
def add_review(request, slug):
    if request.method == "POST" and request.user.is_authenticated:
        product = get_object_or_404(Product, slug=slug)
        form = ReviewForm(request.POST)

        has_paid_order = OrderItem.objects.filter(
            order__user=request.user,
            order__is_paid=True,
            product=product
        ).exists()

        if not has_paid_order:
            return JsonResponse({'success': False, 'error': 'Вы можете оставить отзыв только после оплаты товара.'})

        if Review.objects.filter(user=request.user, product=product).exists():
            return JsonResponse({'success': False, 'error': 'Вы уже оставили отзыв.'})

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return JsonResponse({
                'success': True,
                'username': request.user.username,
                'rating': review.rating,
                'comment': review.comment,
            })
        else:
            return JsonResponse({'success': False, 'error': 'Некорректные данные формы.'})

    return JsonResponse({'success': False, 'error': 'Недопустимый метод запроса.'})
