from django.contrib.auth import authenticate,logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from api.mixin import UltraModelMixin,UserModelMixin
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import *
from .serializers import *
from ..permissions import IsOwnerUser


class ProfileViewSet(UserModelMixin):
    queryset = User.objects.all()
    query = User
    http_method_names = ['get', 'put', 'patch', 'delete']
    serializer_classes = {
        'list': ProfileUserSerializer,
        'retrieve': ProfileUserSerializer,
        'create': ProfileUserSerializer,
        'update': ProfileUserUpdateSerializer,
        'destroy':ProfileUserUpdateSerializer
    }
    permission_classes_by_activ = {
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated | IsAdminUser],
        'update': [IsAuthenticated , IsOwnerUser | IsAdminUser],
        'destroy':[IsAuthenticated , IsOwnerUser | IsAdminUser]
    }

class LoginAPIView(GenericAPIView):
    queryset = Token.objects
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

        read_serializer = ProfileUserSerializer(user)

        date = {
            **read_serializer.data,
            "token":token
        }

        return  Response(date,status.HTTP_201_CREATED)


class ChangPassword(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ChengPasswordSerializer

    def post(self,request,*args,**kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data.get("new_password")
        old_password = serializer.validated_data.get("old_password")

        user = request.user

        if user.check_password(old_password):

            if not user.check_password(new_password):
                user.set_password(new_password)
                user.save()

                return  Response({'default':'Пароль успешно изменён'})

            return Response({'detail':'Пароль должен отличатся от старога'},status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"detail": "Неверный старый пароль"}, status=status.HTTP_400_BAD_REQUEST
        )


class LogoutApiView(GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        # Проверка, что пользователь аутентифицирован
        if user:
            logout(request)
            # Удаление токена пользователя
            Token.objects.filter(user=user).delete()

            return Response({"detail": "Вы успешно вышли из системы."}, status=status.HTTP_200_OK)

        # Сообщение об ошибке, если пользователь не аутентифицирован
        return Response({"detail": "Пользователь не аутентифицирован."}, status=status.HTTP_400_BAD_REQUEST)
