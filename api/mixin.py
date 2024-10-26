from django.core.validators import MinValueValidator
from django.db.models.fields import return_None
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet

from account.models import User
from api.carts.serializers import CartSerializer
from api.orders.serializers import OrdersSerializer
from api.permissions import IsOwnerUser
from carts.models import Cart
from orders.models import Order


class MultipleDestroyMixinSerializer(serializers.Serializer):
    ids = serializers.ListSerializer(child=serializers.IntegerField(validators=[MinValueValidator(1)]))


class MultipleDestroyMixin:
    multiple_delete_permission = permission_classes

    @swagger_auto_schema(request_body=MultipleDestroyMixinSerializer,
                         responses={201: MultipleDestroyMixinSerializer(many=False), 400: 'Bad Request'})
    @permission_classes([multiple_delete_permission])
    @action(methods=['POST'], url_path='multiple-delete', detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        queryset = self.get_queryset()
        items = queryset.filter(id__in=serializer.data['ids'])
        not_deleted_items = []
        for item in items:
            item_id = item.id
            try:
                item.delete()
            except django.db.models.deletion.ProtectedError as e:
                not_deleted_items.append(item_id)
        return Response({
            'not_deleted_items': not_deleted_items
        }, status=status.HTTP_204_NO_CONTENT if len(not_deleted_items) == 0 else status.HTTP_423_LOCKED)

    def get_serializer_class(self):
        path = self.request.path.split('/')[-2]
        if path == 'multiple-delete':
            return MultipleDestroyMixinSerializer
        return super().get_serializer_class()

class SerializerByActive:
    serializer_classes = {}

    def get_serializer_class(self):
        if self.action == 'partial_update' or self.action == 'update_partial':
            return self.serializer_classes.get('update', self.serializer_class)
        return self.serializer_classes.get(self.action, self.serializer_class)



class PermissionByAction:

    permission_classes_by_activ = {}

    def get_permissions(self):
        permission_classes = self.permission_classes_by_activ.get(self.action,None)
        if self.action == 'partial_update' or self.action == 'update_partial':
            permission_classes = self.permission_classes_by_activ.get('update', None)
        if permission_classes is None:
            permission_classes = self.permission_classes

        return  [permission() for permission in permission_classes]

class GetAllItemsMixin:
    serializer_classes = {}

    @action(["GET"], False, "all-items")
    def get_all_items(self, request):

        queryset = self.get_queryset()
        serializer = self.serializer_classes.get('list')(queryset, many=True)

        return Response(serializer.data)

class GetPostAllAccessoriesMixin:

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(user=request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        user_id = User.objects.get(phone=user.phone)

        if user_id.id != serializer.validated_data.get('user').id:
            return Response(
                {
                    'detail': 'Переданно данные другого пользователя'
                }
                , status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

class CountSerializer(serializers.Serializer):
    count_product = serializers.IntegerField()

class StatusSerializer(serializers.Serializer):
    PENDING = 'Pending'  # Ожидание
    IN_PROGRESS = 'In Progress'  # В процессе
    DELIVERED = 'Delivered'  # Доставлен
    CANCELLED = 'Cancelled'  # Отменен

    STATUS_CHOICES = [
        (PENDING, 'Ожидание'),
        (IN_PROGRESS, 'В процессе'),
        (DELIVERED, 'Доставлен'),
        (CANCELLED, 'Отменен'),
    ]

    status = serializers.ChoiceField(choices=STATUS_CHOICES)

class CancelCardByClient:
    serializer_classes = {}

    @swagger_auto_schema(request_body=StatusSerializer,
                         operation_description="Отмена товара.",
                         responses={201: StatusSerializer(many=False), 400: 'Bad Request'})
    @permission_classes([IsAuthenticated, IsOwnerUser | IsAdminUser])
    @action(['POST'], False, 'cancel-order-by-client/(?P<pk>[^/.]+)')
    def cancel_order_by_client(self, request, pk, *args, **kwargs):
        queryset = get_object_or_404(self.get_queryset(), pk=pk)

        user_request = request.user
        user = User.objects.get(phone=user_request.phone)

        if queryset.user != user:
            return Response(
                {
                    'default': 'Предоставлин чужой объект',

                },
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset.status = 'Cancelled'
        queryset.save()

        serializer = self.serializer_classes.get('retrieve')(queryset)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CountSerializer,
        operation_description="Изменяет количество товара в заказе.",
        responses={201: CountSerializer(many=False), 400: 'Bad Request'}
    )
    @permission_classes([IsAuthenticated, IsOwnerUser])
    @action(methods=['POST'], detail=False, url_path='change-product-quantity/(?P<pk>[^/.]+)')
    def change_product_quantity(self, request, pk, *args, **kwargs):
        # Получение объекта корзины по pk
        queryset = get_object_or_404(self.get_queryset(), pk=pk)

        # Проверка и обновление количества товара
        count = request.data.get('count_product')
        if count is not None:
            try:
                count = int(count)
                if count < 1:
                    raise ValidationError("Количество товара должно быть больше 0.")
            except ValueError:
                raise ValidationError("Количество товара должно быть числом.")

            queryset.count_product = count

            queryset.final_tootle_prise =  queryset.count_product * queryset.product.price
            queryset.save()

            # Сериализация обновленного объекта и возврат ответа
            serializer = CartSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Если параметр count не передан
        return Response(
            {"detail": "Параметр 'count' обязателен."},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(['GET'],False,'get-all-status')
    def get_all_status(self,request,*args,**kwargs):

        return Response({
            'PENDING' : 'Ожидание' ,
            'IN_PROGRESS' : 'В процессе' ,
            'DELIVERED':'Доставлен',
            'CANCELLED' : 'Отменен'
        })

class UserOwnerMixin:

    def list(self, request, *args, **kwargs):
        user_request = request.user

        user = get_object_or_404(User, phone=user_request.phone)

        serializer = self.get_serializer(user)
        print(serializer.data)
        return Response(serializer.data)

class UserOwnerDestroyMixin:
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        print(kwargs)
        user_request = request.user
        print(user_request)
        queryset = get_object_or_404(self.query, pk=pk)
        print(queryset)

        if not (queryset == user_request or request.user.is_superuser):
            return Response({
                'default': 'Вы не имеете доступ'

            }, status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

class UserOwnerDestroyListMixin(UserOwnerDestroyMixin,UserOwnerMixin):
    ...


class UserOwnerCartsMixin:

    def list(self, request, *args, **kwargs):
        user_request = request.user

        carts = self.queryset.filter(user=user_request)

        final_prise = sum(item.final_tootle_prise for item in carts)

        serializer = self.get_serializer(carts, many=True)

        data = {
            'carts': serializer.data,
            'final_prise': final_prise
        }

        return Response(data)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

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

            reade_serializer = self.get_serializer(cart)

            return Response(reade_serializer.data,status.HTTP_201_CREATED)
        else:
            return super().create(request,*args,**kwargs)




class BaseModelMixin(
    SerializerByActive,
    PermissionByAction,
):
    ...

class CartsModelMixin(
    BaseModelMixin,
    CancelCardByClient,
    UserOwnerDestroyMixin,
    UserOwnerCartsMixin,
    ModelViewSet,
):
    ...

class UltraModelMixin(
    BaseModelMixin,
    GetAllItemsMixin,
    ModelViewSet
): ...

class A2UModelMixin(
    BaseModelMixin,
    UserOwnerDestroyListMixin,
    MultipleDestroyMixin,
    GetPostAllAccessoriesMixin,
    GetAllItemsMixin,
    ModelViewSet
): ...


class UserModelMixin(
    BaseModelMixin,
    UserOwnerMixin,
    ModelViewSet
): ...