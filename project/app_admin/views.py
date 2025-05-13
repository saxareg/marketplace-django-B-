from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from .forms import LoginForm, ShopForm, ProductForm, CategoryForm, PickupPointForm
from app_orders.models import Order, Cart
from app_products.models import Product, Category, Review
from app_shops.models import Shop, ShopCreationRequest
from app_users.models import PickupPoints
from app_users.forms import UserProfileUpdateForm
from .forms import ReviewForm


User = get_user_model()


def is_superuser(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_superuser, login_url='/custom_admin/login/')
def cart_detail(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    items = cart.items.select_related('product')
    return render(request, 'admin/cart_detail.html', {
        'cart': cart,
        'items': items,
        'model': 'Cart'
    })


def admin_login(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('app_admin:dashboard')
        else:
            form.add_error(None, 'Доступ разрешён только суперпользователям.')
    return render(request, 'admin/login.html', {'form': form})


def admin_logout(request):
    logout(request)
    return redirect('app_admin:login')


# Dashboard
@user_passes_test(is_superuser, login_url='/custom_admin/login/')
def dashboard(request):
    sections = [
        {"name": "Магазины", "url": reverse('app_admin:shop_list'), "icon": "bi-shop"},
        {"name": "Заявки", "url": reverse('app_admin:shoprequest_list'), "icon": "bi-journal-text"},
        {"name": "Пункты самовывоза", "url": reverse('app_admin:pickup_list'), "icon": "bi-geo-alt"},
        {"name": "Заказы", "url": reverse('app_admin:order_list'), "icon": "bi-basket"},
        {"name": "Товары", "url": reverse('app_admin:product_list'), "icon": "bi-box-seam"},
        {"name": "Категории", "url": reverse('app_admin:category_list'), "icon": "bi-tags"},
        {"name": "Отзывы", "url": reverse('app_admin:review_list'), "icon": "bi-chat-dots"},
        {"name": "Пользователи", "url": reverse('app_admin:user_list'), "icon": "bi-people"},
    ]
    return render(request, 'admin/dashboard.html', {"sections": sections})


def generate_crud(model, form_class, model_name):

    @user_passes_test(is_superuser, login_url='/custom_admin/login/')
    def list_view(request):
        items = model.objects.all()
        model_slug = model_name.lower()
        can_create = form_class is not None
        return render(request, 'admin/model_list.html', {
            'items': items,
            'model': model_name,
            'model_slug': model_slug,
            'can_create': can_create
        })

    @user_passes_test(is_superuser, login_url='/custom_admin/login/')
    def create_view(request):
        if form_class is None:
            return redirect(request.path.replace('/create/', '/'))
        form = form_class(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect(request.path.replace('/create/', '/'))
        return render(request, 'admin/model_create.html', {'form': form, 'model': model_name})

    @user_passes_test(is_superuser, login_url='/custom_admin/login/')
    def update_view(request, pk):
        obj = get_object_or_404(model, pk=pk)
        if form_class is None:
            return redirect(request.path.replace(f'/{pk}/update/', '/'))
        form = form_class(request.POST or None, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(request.path.replace(f'/{pk}/update/', '/'))
        return render(request, 'admin/model_update.html', {'form': form, 'model': model_name})

    @user_passes_test(is_superuser, login_url='/custom_admin/login/')
    def delete_view(request, pk):
        obj = get_object_or_404(model, pk=pk)
        obj.delete()
        return redirect(request.path.replace(f'/{pk}/delete/', '/'))

    return list_view, create_view, update_view, delete_view


shop_list, shop_create, shop_update, shop_delete = generate_crud(Shop, ShopForm, "Shop")
shoprequest_list, _, _, shoprequest_delete = generate_crud(ShopCreationRequest, None, "ShopRequest")
pickup_list, pickup_create, pickup_update, pickup_delete = generate_crud(PickupPoints, PickupPointForm, "PickupPoint")
order_list, _, order_update, order_delete = generate_crud(Order, None, "Order")
product_list, product_create, product_update, product_delete = generate_crud(Product, ProductForm, "Product")
category_list, category_create, category_update, category_delete = generate_crud(Category, CategoryForm, "Category")
review_list, review_create, review_update, review_delete = generate_crud(Review, ReviewForm, "Review")


# User admin
@user_passes_test(is_superuser, login_url='/custom_admin/login/')
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin/model_list.html', {
        'items': users,
        'model': 'User',
        'model_slug': 'user',
        'can_create': False
    })


@user_passes_test(is_superuser, login_url='/custom_admin/login/')
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserProfileUpdateForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('app_admin:user_list')
    return render(request, 'admin/model_update.html', {'form': form, 'model': 'User'})


@user_passes_test(is_superuser, login_url='/custom_admin/login/')
def approve_shop_request(request, pk):
    request_obj = get_object_or_404(ShopCreationRequest, pk=pk)
    if request_obj.status != 'pending':
        return redirect('app_admin:shoprequest_list')

    Shop.objects.create(
        name=request_obj.name,
        slug=request_obj.slug,
        description=request_obj.description,
        logo=request_obj.logo,
        owner=request_obj.user
    )

    request_obj.status = 'approved'
    request_obj.response_time = now()
    request_obj.save()

    send_mail(
        subject='Ваш магазин одобрен!',
        message=(
            f'Здравствуйте, {request_obj.user.username}!\n\n'
            f'Ваша заявка на создание магазина "{request_obj.name}" была одобрена. '
            f'Теперь вы можете управлять своим магазином в системе.\n\n'
            'С уважением,\nАдминистрация Marketplace'
        ),
        from_email=None,
        recipient_list=[request_obj.user.email],
        fail_silently=False,
    )

    return redirect('app_admin:shoprequest_list')


@user_passes_test(is_superuser, login_url='/custom_admin/login/')
def reject_shop_request(request, pk):
    request_obj = get_object_or_404(ShopCreationRequest, pk=pk)
    if request_obj.status != 'pending':
        return redirect('app_admin:shoprequest_list')

    request_obj.status = 'rejected'
    request_obj.response_time = now()
    request_obj.save()

    send_mail(
        subject='Заявка на создание магазина отклонена',
        message=(
            f'Здравствуйте, {request_obj.user.username}!\n\n'
            f'К сожалению, ваша заявка на создание магазина "{request_obj.name}" была отклонена.\n'
            f'Вы можете связаться с администрацией для уточнения причин.\n\n'
            'С уважением,\nАдминистрация Marketplace'
        ),
        recipient_list=[request_obj.user.email],
        fail_silently=False,
    )

    return redirect('app_admin:shoprequest_list')
