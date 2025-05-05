from django import forms
from app_shops.models import Shop
from app_orders.models import Order
from app_products.models import Product, Category
from app_users.models import PickupPoints

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
        model = PickupPoint
        fields = '__all__'
