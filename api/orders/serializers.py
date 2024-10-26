from rest_framework.generics import get_object_or_404

from orders.models import Order,PromotionalCode
from main.models import Product
from account.models import User
from  api.serializers import ProductListSerializer

from rest_framework import serializers

class OrdersSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = Order
        fields = [
            'id',
            'product',
            'user',
            'count',
            'status',
            'total_price',
            'promo_code',
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    promo_code = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = [
            'product',
            'user',
            'count',
            'promo_code'
        ]

    def save(self, **kwargs):
        # Получаем промокод из данных
        promo_code_name = self.validated_data.pop('promo_code', None)
        promo_code_instance = None  # Переменная для хранения экземпляра промокода

        if promo_code_name:
            # Ищем промокод по названию
            try:
                promo_code_instance = PromotionalCode.objects.get(code=promo_code_name)
            except PromotionalCode.DoesNotExist:
                raise serializers.ValidationError("Промокод не существует.")

        # Создаем заказ с актуальными данными
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