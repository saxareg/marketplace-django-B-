from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

from app_shops.models import Shop
from app_products.models import Product
from api_public.serializers import ShopSerializer
from api_seller.serializers import ProductSerializer

class SellerShopListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer

    @extend_schema(
        operation_id='seller_list',
        description='Получение списка магазинов текущего пользователя'
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Shop.objects.none()  # Возвращаем пустой Queryset для drf-spectacular
        return Shop.objects.filter(owner=self.request.user).order_by("id")

class SellerShopDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer
    lookup_field = 'slug'

    @extend_schema(
        operation_id='seller_detail',
        description='Получение или обновление магазина по slug'
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Shop.objects.none()  # Добавляем для консистентности
        return Shop.objects.filter(owner=self.request.user)

class SellerProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    @extend_schema(
        operation_id='seller_product_list',
        description='Получение списка товаров магазина',
        parameters=[
            OpenApiParameter(
                name='shop_slug',
                type=str,
                location=OpenApiParameter.PATH,
                description='Slug магазина'
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id='seller_product_create',
        description='Создание нового товара в магазине',
        parameters=[
            OpenApiParameter(
                name='shop_slug',
                type=str,
                location=OpenApiParameter.PATH,
                description='Slug магазина'
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        operation_id='seller_product_retrieve',
        description='Получение товара по slug',
        parameters=[
            OpenApiParameter(
                name='shop_slug',
                type=str,
                location=OpenApiParameter.PATH,
                description='Slug магазина'
            ),
            OpenApiParameter(
                name='slug',
                type=str,
                location=OpenApiParameter.PATH,
                description='Slug товара'
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id='seller_product_update',
        description='Обновление товара по slug',
        parameters=[
            OpenApiParameter(
                name='shop_slug',
                type=str,
                location=OpenApiParameter.PATH,
                description='Slug магазина'
            ),
            OpenApiParameter(
                name='slug',
                type=str,
                location=OpenApiParameter.PATH,
                description='Slug товара'
            )
        ]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        operation_id='seller_product_delete',
        description='Удаление товара по slug',
        parameters=[
            OpenApiParameter(
                name='shop_slug',
                type=str,
                location=OpenApiParameter.PATH,
                description='Slug магазина'
            ),
            OpenApiParameter(
                name='slug',
                type=str,
                location=OpenApiParameter.PATH,
                description='Slug товара'
            )
        ]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Product.objects.none()
        shop_slug = self.kwargs["shop_slug"]
        shop = Shop.objects.filter(slug=shop_slug, owner=self.request.user).first()
        if not shop:
            raise PermissionDenied("Магазин не найден или не принадлежит вам.")
        return Product.objects.filter(shop=shop).order_by("id")

    def perform_create(self, serializer):
        shop_slug = self.kwargs['shop_slug']
        shop = get_object_or_404(Shop, slug=shop_slug, owner=self.request.user)
        serializer.save(shop=shop)
