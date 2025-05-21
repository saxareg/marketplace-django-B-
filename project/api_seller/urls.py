from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_seller.views import (
    SellerShopListView,
    SellerShopDetailView,
    SellerProductViewSet,
)

product_router = DefaultRouter()
product_router.register(r'', SellerProductViewSet, basename='shop-products')

urlpatterns = [
    path("", SellerShopListView.as_view(), name="seller-shop-list"),
    path("<slug:slug>/", SellerShopDetailView.as_view(), name="seller-shop-detail"),
    path("<slug:shop_slug>/products/", include(product_router.urls)),
]
