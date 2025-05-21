from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_public.views import ProductViewSet, CategoryViewSet, ShopViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='public-products')
router.register(r'categories', CategoryViewSet, basename='public-categories')
router.register(r'shops', ShopViewSet, basename='public-shops')

urlpatterns = router.urls  # ✅ просто отдаём router.urls напрямую
