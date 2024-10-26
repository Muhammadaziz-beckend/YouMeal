from rest_framework import serializers

from carts.models import Cart
from main.models import Product
from api.serializers import ProductListSerializer

class CartSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = Cart
        fields = '__all__'


class CartCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Cart
        fields = [
            'user',
            'product',
            'count_product',
        ]

class CartDestroySerializer(serializers.Serializer):
    id = serializers.IntegerField()