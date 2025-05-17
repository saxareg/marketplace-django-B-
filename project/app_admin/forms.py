from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

# Importing models from various apps
from app_shops.models import Shop
from app_orders.models import Order, Cart
from app_products.models import Product, Category, Review
from app_users.models import PickupPoints

# Get the custom user model
User = get_user_model()


# Form for the shopping cart
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'  # Include all fields from the Cart model


# Form for submitting product reviews
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'  # Include all fields from the Review model


# Custom login form with Bootstrap styling
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# Form for creating or editing a shop
class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = '__all__'


# Form for creating or editing an order
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


# Form for adding or editing a product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


# Form for adding or editing a category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


# Form for managing pickup points (delivery locations)
class PickupPointForm(forms.ModelForm):
    class Meta:
        model = PickupPoints
        fields = '__all__'
