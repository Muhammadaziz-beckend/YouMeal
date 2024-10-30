from rest_framework.filters import OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.permissions import *

from .mixin import GetAllObjUser
from ..mixin import BaseModelMixin
from orders.models import Order
from ..orders.serializers import OrdersSerializer
from ..paginators import PaginatorProduct

class BaseOrderViewSet(GetAllObjUser, BaseModelMixin):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering = ['date_create', 'total_price', 'type_order']
    http_method_names = ['get', ]
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginatorProduct

class OrdersViewSet(BaseOrderViewSet):
    queryset = Order.objects.all().exclude(status__in=[Order.DELIVERED, Order.CANCELLED])

class HistoryViewSet(BaseOrderViewSet):
    queryset = Order.objects.filter(status__in=[Order.DELIVERED, Order.CANCELLED])