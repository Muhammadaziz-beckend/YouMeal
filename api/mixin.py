from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action,permission_classes

from api.serializers import ProductListSerializer
from rest_framework.mixins import  ListModelMixin


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
        print(self.action,'--------------------')
        queryset = self.get_queryset()
        # serializer = self.get_serializer(queryset,many=True)
        serializer = self.serializer_classes.get('list')(queryset, many=True)

        return Response(serializer.data)

class UltraModelMixin(GetAllItemsMixin,SerializerByActive,PermissionByAction,ModelViewSet):
    ...