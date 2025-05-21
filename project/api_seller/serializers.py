from rest_framework import serializers
from app_products.models import Product, Category
from app_shops.models import Shop


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'category', 'shop']
        read_only_fields = ['shop']

    def validate_shop(self, shop):
        user = self.context["request"].user
        if shop.owner != user:
            raise serializers.ValidationError("Вы не владелец этого магазина.")
        return shop