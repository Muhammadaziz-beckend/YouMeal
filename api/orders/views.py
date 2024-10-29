from django.core.serializers import serialize
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from orders.models import Order, STATUS, PromotionalCode, Address
from account.models import User
from api.auth.serializers import ProfileUserSerializer
from .serializers import OrdersSerializer, OrderCreateSerializer, PromotionalCodeCreateSerializer, \
    PromotionalCodeSerializer, AddressSerializer
from api.mixin import UltraModelMixin, A2UModelMixin, UserOwnerDestroyListMixin, GetAllAddressIsOwnerMixin
from api.permissions import IsOwnerUser

from rest_framework.permissions import *
from rest_framework.filters import  OrderingFilter

class OrdersViewSet(UserOwnerDestroyListMixin,A2UModelMixin):
    queryset = Order.objects.all()
    query = Order
    user_get_all_items = True
    lookup_field = 'id'
    serializer_classes = {
        'list': OrdersSerializer,
        'retrieve':OrdersSerializer,
        'create': OrderCreateSerializer,
        'update': OrderCreateSerializer
    }
    filter_backends = [OrderingFilter]
    ordering = ['count','status','date_create','total_price']
    permission_classes_by_activ = {
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated , IsOwnerUser | IsAdminUser],
        'update': [IsAuthenticated , IsOwnerUser | IsAdminUser]
    }

class PromotionalCodeViewSet(UltraModelMixin):
    queryset = PromotionalCode.objects.all()
    lookup_field = 'id'
    serializer_classes = {
        'list': PromotionalCodeSerializer,
        'retrieve': PromotionalCodeSerializer,
        'create': PromotionalCodeCreateSerializer,
        'update': PromotionalCodeCreateSerializer
    }
    permission_classes_by_activ = {
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated, IsOwnerUser | IsAdminUser],
        'update': [IsAuthenticated, IsOwnerUser | IsAdminUser]
    }


class AddressViewSet(GetAllAddressIsOwnerMixin,A2UModelMixin):
    queryset = Address.objects.all()
    user_items = True
    lookup_field = 'id'
    serializer_classes = {
        'list': AddressSerializer,
        'retrieve': AddressSerializer,
        'create': AddressSerializer,
        'update': AddressSerializer
    }
    permission_classes_by_activ = {
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated, IsOwnerUser | IsAdminUser],
        'update': [IsAuthenticated, IsOwnerUser | IsAdminUser]
    }

