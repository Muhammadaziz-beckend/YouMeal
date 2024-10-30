from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import *
from rest_framework.response import Response

from api.mixin import CartsModelMixin

from .serializers import *
from ..permissions import IsOwnerUser, IsIdEUser, IsOwnerCard


class CardsViewSet(CartsModelMixin):
    queryset = Cart.objects.filter(is_see_user=True)
    lookup_field = 'id'
    query = Cart
    serializer_classes = {
        'list':CartSerializer,
        'retrieve':CartSerializer,
        'create':CartCreateSerializer,
        'update':CartCreateSerializer,
        'destroy':CartDestroySerializer
    }
    permission_classes_by_activ = {
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated, IsAdminUser],
        'update': [IsAuthenticated, IsOwnerUser | IsAdminUser],
        'destroy': [IsAuthenticated, IsOwnerCard | IsAdminUser],
    }