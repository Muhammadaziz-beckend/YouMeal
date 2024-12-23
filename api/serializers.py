from rest_framework import  serializers

from main.models import *
from orders.models import *

class ProductCompositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product_composition
        fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):
    product_composition = ProductCompositionSerializer(many=True)

    class Meta:
        model = Product
        exclude = ['date_update']

class ProductCreteSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = [
            'image',
            'name',
            'description',
            'weight',
            'calories',
            'price',
            'category'
        ]

    # def create(self, validated_data):
    #
    #
    #
    #     return

class ProductRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'icon',
            'name'
        ]


class OrdersListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

from account.models import  User
class OrdersCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Order
        fields = [
            'product',  'user',  'count',
        ]