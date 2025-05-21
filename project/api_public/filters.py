from django_filters import rest_framework as filters
from app_products.models import Product


class BaseInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    category__slug = filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    category__slug__in = BaseInFilter(field_name='category__slug', lookup_expr='in')
    shop__slug = filters.CharFilter(field_name='shop__slug', lookup_expr='exact')
    shop__slug__in = BaseInFilter(field_name='shop__slug', lookup_expr='in')

    class Meta:
        model = Product
        fields = []
