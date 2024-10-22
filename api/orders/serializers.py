from orders.models import Order
from main.models import Product
from account.models import User

from rest_framework import serializers

class OrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'id',
            'product',
            'user',
            'count',
            'status',
            'total_price',
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Order
        fields = [
            'product',
            'user',
            'count',
        ]