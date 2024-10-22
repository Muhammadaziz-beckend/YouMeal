from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from api.mixin import UltraModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import *
from .serializers import *

class ProfileViewSet(UltraModelMixin):
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_classes = {
        'list': ProfileUserSerializer,
        'retrieve': ProfileUserSerializer,
        'create': ProfileUserSerializer,
        'update': ProfileUserSerializer
    }
    permission_classes_by_activ = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated | IsAdminUser],
        'update': [IsAuthenticated | IsAdminUser]
    }

class LoginAPIView(GenericAPIView):
    queryset = Token.objects.all()
    serializer_class = LoginSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data.get("phone")
        password = serializer.validated_data.get("password")

        user = authenticate(phone=phone, password=password)

        if user:
            reade_serializer = ProfileUserSerializer(
                instance=user, context={"request": request}
            )

            token = self.get_queryset().get_or_create(user=user)[0].key

            date = {
                **reade_serializer.data,
                "token": token,
            }

            return Response(date)

        return Response(
            {"detail": "Пользователь не существует или пароль неверен"},
            status.HTTP_401_UNAUTHORIZED,
        )

class RegisterAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self,request,*args,**kwargs):
        phone = request.data.get('phone')

        serializer:RegisterSerializer = self.get_serializer(data=request.data)

        if self.get_queryset().filter(phone=phone):

            return  Response(
                {
                    "detail": "Такой телефон номер уже существует"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        token = Token.objects.get_or_create(user=user)[0].key

        read_serializer = ProfileUserSerializer(instance=user)

        date = {
            **read_serializer,
            "token":token
        }

        return  Response(date,status.HTTP_201_CREATED)


