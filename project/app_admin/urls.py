from django.urls import path
from . import views

app_name = 'app_admin'

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('logout/', views.admin_logout, name='logout'),

    path('shops/', views.shop_list, name='shop_list'),
    path('shops/create/', views.shop_create, name='shop_create'),
    path('shops/<int:pk>/edit/', views.shop_update, name='shop_update'),
    path('shops/<int:pk>/delete/', views.shop_delete, name='shop_delete'),

    path('shoprequests/', views.shoprequest_list, name='shoprequest_list'),
    path('shoprequests/<int:pk>/delete/', views.shoprequest_delete, name='shoprequest_delete'),
    path('shoprequests/<int:pk>/approve/', views.approve_shop_request, name='shoprequest_approve'),
    path('shoprequests/<int:pk>/reject/', views.reject_shop_request, name='shoprequest_reject'),

    path('pickups/', views.pickup_list, name='pickup_list'),
    path('pickups/create/', views.pickup_create, name='pickuppoint_create'),
    path('pickups/<int:pk>/edit/', views.pickup_update, name='pickuppoint_update'),
    path('pickups/<int:pk>/delete/', views.pickup_delete, name='pickuppoint_delete'),

    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/edit/', views.order_update, name='order_update'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),

    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('carts/', views.cart_list, name='cart_list'),
    path('carts/<int:pk>/delete/', views.cart_delete, name='cart_delete'),

    path('reviews/', views.review_list, name='review_list'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),

    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/edit/', views.user_update, name='user_update'),
]

