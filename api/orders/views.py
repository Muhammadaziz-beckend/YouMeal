from django.core.serializers import serialize
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from orders.models import Order, STATUS
from account.models import User
from api.auth.serializers import ProfileUserSerializer
from .serializers import OrdersSerializer,OrderCreateSerializer
from api.mixin import UltraModelMixin,A2UModelMixin
from api.permissions import IsOwnerUser

from rest_framework.permissions import *
from rest_framework.filters import  OrderingFilter

class OrdersViewSet(A2UModelMixin):
    queryset = Order.objects.all()
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

