from rest_framework.serializers import  ModelSerializer,Serializer
from rest_framework import serializers

from account.models import User

# class UserSerializer(ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = []


class RegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'phone',
            'first_name',
            'last_name',
            'email'
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)

        user.set_password(password)

        user.save()

        return user

class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "email",  # +
            "last_name",
            "first_name",
        ]

class LoginSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'phone',
            'password'
        ]

class ChangPasswordSerializer(Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class ProfileUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "get_full_name",
            "last_name",
            "first_name",
            "phone",
            "email",
            "role",
        ]