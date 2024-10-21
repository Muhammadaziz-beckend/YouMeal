from rest_framework import status
from rest_framework.permissions import  *
from rest_framework.decorators import permission_classes, action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from main.models import  *
from orders.models import *
from .mixin import UltraModelMixin
from .paginators import PaginatorProduct

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
    ordering = ["price", "name", "date_create",'weight','calories']
    search_fields = ['name','description','weight','calories','price']
    permission_classes_by_activ = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated | IsAdminUser],
        'update': [IsAuthenticated | IsAdminUser]
    }
    pagination_class = PaginatorProduct


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