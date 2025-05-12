from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from app_shops.models import Shop
from app_orders.models import Order
from app_products.models import Product, Category
from app_users.models import PickupPoints
from django.contrib.auth.forms import AuthenticationForm
from app_orders.models import Cart
from app_products.models import Review


User = get_user_model()

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class PickupPointForm(forms.ModelForm):
    class Meta:
        model = PickupPoints
        fields = '__all__'