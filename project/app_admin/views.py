from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .forms import *

User = get_user_model()

def dashboard(request):
    return render(request, 'app_admin/dashboard.html')


def generate_crud(model, form_class, model_name):
    def list_view(request):
        items = model.objects.all()
        return render(request, 'app_admin/model_list.html', {'items': items, 'model': model_name})

    def create_view(request):
        form = form_class(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect(f'app_admin:{model_name.lower()}_list')
        return render(request, 'app_admin/model_create.html', {'form': form, 'model': model_name})

    def update_view(request, pk):
        obj = get_object_or_404(model, pk=pk)
        form = form_class(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(f'app_admin:{model_name.lower()}_list')
        return render(request, 'app_admin/model_update.html', {'form': form, 'model': model_name})

    def delete_view(request, pk):
        obj = get_object_or_404(model, pk=pk)
        obj.delete()
        return redirect(f'app_admin:{model_name.lower()}_list')

    return list_view, create_view, update_view, delete_view

# Модели и формы
from app_orders.models import Order
from app_products.models import Product, Category, Cart, Review
from app_shops.models import Shop, ShopRequest
from app_users.models import PickupPoints
from app_users.forms import CustomUserChangeForm  # кастомная форма для User

# CRUD
shop_list, shop_create, shop_update, shop_delete = generate_crud(Shop, ShopForm, "Shop")
shoprequest_list, _, _, shoprequest_delete = generate_crud(ShopRequest, None, "ShopRequest")
pickup_list, pickup_create, pickup_update, pickup_delete = generate_crud(PickupPoint, PickupPointForm, "PickupPoint")
order_list, _, order_update, order_delete = generate_crud(Order, OrderForm, "Order")
product_list, product_create, product_update, product_delete = generate_crud(Product, ProductForm, "Product")
category_list, category_create, category_update, category_delete = generate_crud(Category, CategoryForm, "Category")
cart_list, _, _, cart_delete = generate_crud(Cart, None, "Cart")
review_list, _, _, review_delete = generate_crud(Review, None, "Review")

def user_list(request):
    users = User.objects.all()
    return render(request, 'app_admin/model_list.html', {'items': users, 'model': 'User'})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = CustomUserChangeForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('app_admin:user_list')
    return render(request, 'app_admin/model_update.html', {'form': form, 'model': 'User'})
from django.shortcuts import render


