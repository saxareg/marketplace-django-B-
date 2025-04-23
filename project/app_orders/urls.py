from django.urls import path
from . import views

urlpatterns = [
    path('edit/', views.toggle_cart_item, name='toggle_cart_item'),
    path('remove/', views.cart_remove, name='cart_remove'),
    path('', views.cart_view, name='cart')
]
