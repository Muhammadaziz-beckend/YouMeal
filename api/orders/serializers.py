from rest_framework.generics import get_object_or_404

from orders.models import Order, PromotionalCode, Address
from main.models import Product
from account.models import User
from  api.serializers import ProductListSerializer
from ..carts.serializers import *

from rest_framework import serializers

class OrdersSerializer(serializers.ModelSerializer):
    cart = CartSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'address',
            'type_order',
            'status',
            'total_price',
            'promo_code',
            'cart'
        ]

class OrderCreateSerializer(serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    promo_code = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = [
            'user',
            'address',
            'type_order',
            'promo_code',
        ]

    def save(self, **kwargs):
        promo_code_name = self.validated_data.pop('promo_code', None)
        promo_code_instance = None

        if promo_code_name:
            try:
                promo_code_instance = PromotionalCode.objects.get(code=promo_code_name,is_active=True)
            except PromotionalCode.DoesNotExist:
                raise serializers.ValidationError("Промокод не существует.")

        # Создаем заказ
        order = Order.objects.create(promo_code=promo_code_instance, **self.validated_data)
        return order




class PromotionalCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PromotionalCode
        fields = '__all__'


class PromotionalCodeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PromotionalCode
        fields = [
            'code',
            'discount_type',
            'subtraction_from_the_amount',
            'data_start',
            'data_end',
            'is_active'
        ]

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'