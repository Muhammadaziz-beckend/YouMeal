from rest_framework.response import Response


class GetAllObjUser:
    def list(self,request,*args,**kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(user__phone=request.user.phone))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user.phone != request.user.phone:
            raise PermissionDenied("Вы не имеете доступа к этому заказу.")

        serializer = self.get_serializer(instance)
        return Response(serializer.data)