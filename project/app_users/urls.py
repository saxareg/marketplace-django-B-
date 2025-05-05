from django.urls import path
from . import views
from app_orders.views import pp_order_detail_view

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('me/', views.profile_view, name='me'),
    path('pickup-point/', views.pp_view, name='my-pp'),
    path('pickup-point/order/<int:order_id>/', pp_order_detail_view, name='order-detail'),
]
