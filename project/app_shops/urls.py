from django.urls import path
from . import views


urlpatterns = [
    path('my-shops/', views.my_shops_view, name='my-shops'),
    path('my-shops/<slug:slug>/', views.my_shop_detail, name='shop-detail'),
    path('create/', views.shop_create_request, name='shop-create-request'),
    path('delete/<slug:slug>/', views.shop_delete, name='shop-delete'),
    path('my-shops/<slug:slug>/toggle-status/', views.toggle_shop_status, name='toggle_shop_status'),
]
