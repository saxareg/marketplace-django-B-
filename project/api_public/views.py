from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist

from app_products.models import Product, Category
from app_shops.models import Shop
from api_public.serializers import ProductSerializer, CategorySerializer, ShopSerializer
from api_public.filters import ProductFilter


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ShopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Shop.objects.all().order_by("id")
    serializer_class = ShopSerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name']
    ordering_fields = ['price', 'name']
    ordering = ['name']

    def get_queryset(self):
        q = self.request.query_params

        category_slug = q.get("category__slug")
        category_slug_list = q.get("category__slug__in")
        shop_slug = q.get("shop__slug")
        shop_slug_list = q.get("shop__slug__in")

        if not (q.get("category") or category_slug or category_slug_list):
            raise ValidationError({
                "detail": "You must specify a category filter (by ID or slug) to list products."
            })

        if category_slug and not Category.objects.filter(slug=category_slug).exists():
            raise ValidationError({
                "detail": f"Category with slug '{category_slug}' does not exist."
            })

        if category_slug_list:
            slugs = [s.strip() for s in category_slug_list.split(',')]
            found = set(Category.objects.filter(slug__in=slugs).values_list("slug", flat=True))
            missing = set(slugs) - found
            if missing:
                raise ValidationError({
                    "detail": f"Unknown categories: {', '.join(sorted(missing))}"
                })

        if shop_slug and not Shop.objects.filter(slug=shop_slug).exists():
            raise ValidationError({
                "detail": f"Shop with slug '{shop_slug}' does not exist."
            })

        if shop_slug_list:
            slugs = [s.strip() for s in shop_slug_list.split(',')]
            found = set(Shop.objects.filter(slug__in=slugs).values_list("slug", flat=True))
            missing = set(slugs) - found
            if missing:
                raise ValidationError({
                    "detail": f"Unknown shops: {', '.join(sorted(missing))}"
                })

        return super().get_queryset()
