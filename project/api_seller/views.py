from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from app_shops.models import Shop
from app_products.models import Product
from api_public.serializers import ShopSerializer
from api_seller.serializers import ProductSerializer


class SellerShopListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shops = Shop.objects.filter(owner=request.user).order_by("id")
        return Response(ShopSerializer(shops, many=True).data)


class SellerShopDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer
    lookup_field = "slug"
    queryset = Shop.objects.all()

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied("Это не ваш магазин.")
        return obj


class SellerProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        shop_slug = self.kwargs["shop_slug"]
        shop = Shop.objects.filter(slug=shop_slug, owner=self.request.user).first()
        if not shop:
            raise PermissionDenied("Магазин не найден или не принадлежит вам.")
        return Product.objects.filter(shop=shop).order_by("id")

    def perform_create(self, serializer):
        shop_slug = self.kwargs['shop_slug']
        user = self.request.user
        shop = get_object_or_404(Shop, slug=shop_slug, owner=user)
        if not shop:
            raise PermissionDenied("Нельзя создать товар для чужого магазина.")
        serializer.save(shop=shop)
