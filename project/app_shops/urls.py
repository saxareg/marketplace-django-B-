from django.urls import path
from . import views


urlpatterns = [
    path('my-shops/', views.my_shops_view, name='my-shops'),
    path('my-shops/<slug:slug>/', views.my_shop_detail, name='shop-detail'),
]
