from rest_framework import status
from rest_framework.permissions import  *
from rest_framework.decorators import permission_classes, action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .clone import clone
from .serializers import *
from main.models import  *
from orders.models import *
from .mixin import UltraModelMixin
from .paginators import PaginatorProduct
from .filters import ProductFilter

class ProductViewSet(UltraModelMixin):
    queryset = Product.objects.all()
    lookup_field = 'id'
    serializer_classes = {
        'list': ProductListSerializer,
        'retrieve': ProductRetrieveSerializer,
        'create':ProductCreteSerializer,
        'update':ProductCreteSerializer
    }
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name','description','weight','calories','price']
    filterset_class = ProductFilter
    ordering = ["price", "name", "date_create",'weight','calories']
    permission_classes_by_activ = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated | IsAdminUser],
        'update': [IsAuthenticated | IsAdminUser]
    }
    pagination_class = PaginatorProduct

    # def retrieve(self, request, *args, **kwargs):
    #     product = self.get_object()
    #
    #     # cloned_products = clone(product.id, 500)
    #
    #     serializer = self.get_serializer(product)
    #     return Response(serializer.data)


class CategoryViewSet(UltraModelMixin):
    queryset =  Category.objects.all()
    lookup_field = 'id'
    serializer_classes = {
        'list': CategoryListSerializer,
        'retrieve': CategoryListSerializer,
        'create': CategoryCreateSerializer,
        'update': CategoryCreateSerializer
    }
    permission_classes_by_activ = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated | IsAdminUser],
        'update': [IsAuthenticated | IsAdminUser]
    }


class OrdersViewSet(UltraModelMixin):
    queryset = Order.objects.all()
    lookup_field = 'id'
    serializer_classes = {
        'list': OrdersListSerializer,
        'retrieve': OrdersListSerializer,
        'create': OrdersCreateSerializer,
        'update': OrdersCreateSerializer
    }
    permission_classes_by_activ = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated | IsAdminUser],
        'update': [IsAuthenticated | IsAdminUser]
    }