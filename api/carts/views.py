from rest_framework.generics import get_object_or_404
from rest_framework.permissions import *
from rest_framework.response import Response

from api.mixin import CartsModelMixin

from carts.models import Cart
from .serializers import *
from ..permissions import IsOwnerUser, IsIdEUser, IsOwnerCard


class CardsViewSet(CartsModelMixin):
    queryset = Cart.objects.all()
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
        'create': [IsAuthenticated, IsIdEUser],
        'update': [IsAuthenticated, IsOwnerUser | IsAdminUser],
        'destroy': [IsAuthenticated, IsOwnerCard | IsAdminUser],
    }

    def create(self, request, *args, **kwargs):

        serializer:CartCreateSerializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user']
        product_pk = serializer.validated_data['product']
        count_product = serializer.validated_data['count_product']

        arr = list(self.get_queryset().filter(product=product_pk,user=user_id))
        if len(arr) > 0:
            cart, *carts = arr
            if len(carts) > 0:
                for i in carts:
                    cart.count_product += i.count_product
                    i.delete()

            cart.count_product += count_product
            cart.save()

            print(cart,carts,arr)

            reade_serializer = self.get_serializer(cart)

            return Response(reade_serializer.data)
        else:
            return super().create(request,*args,**kwargs)