from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, Category
from app_orders.models import Cart, CartItem, OrderItem
from app_shops.models import Shop
from .forms import ProductForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Min, Max
from urllib.parse import urlencode


def product_list(request):
    """
    Display a list of products with optional filters: search query, category, and price range.
    Includes pagination and category display.
    """

    categories = Category.objects.all()
    price_min_limit = Product.objects.aggregate(Min('price'))['price__min'] or 0
    price_max_limit = Product.objects.aggregate(Max('price'))['price__max'] or 10000

    query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')
    try:
        min_price = float(request.GET.get('min_price', price_min_limit))
        max_price = float(request.GET.get('max_price', price_max_limit))
    except ValueError:
        min_price = price_min_limit
        max_price = price_max_limit

    products = Product.objects.all().order_by('id')
    if query:
        products = products.filter(name__icontains=query)
    if selected_category:
        products = products.filter(category_id=selected_category)

    products = products.filter(price__gte=min_price, price__lte=max_price)
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    query_params = urlencode({
        'q': query,
        'category': selected_category,
        'min_price': min_price,
        'max_price': max_price,
    })
    context = {
        'categories': categories,
        'page_obj': page_obj,
        'price_min_limit': price_min_limit,
        'price_max_limit': price_max_limit,
        'min_price': min_price,
        'max_price': max_price,
        'selected_category': selected_category,
        'query_params': query_params,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, slug):
    """
    Display the product detail page, including whether it's in the user's cart,
    if the user is the shop owner, and whether the user can leave a review.
    """

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
    """Allow shop owner to delete a product. Redirect to shop page after deletion."""

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
    """Allow shop owner to edit an existing product."""

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
    """Allow shop owner to create a new product in their shop."""

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
    """
    Allow a user to submit a review if they have purchased and paid for the product.
    Returns JSON response with review data or error message.
    """

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
