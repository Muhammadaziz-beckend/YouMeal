from rest_framework import  permissions
from rest_framework.generics import get_object_or_404

from account.models import User

class IsOwnerUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return  True

        return (obj.phone == request.user.phone) or request.user.is_superuser

class IsOwnerCard(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return  True

        return obj.user_id == request.user.id or request.user.is_superuser


class IsIdEUser(permissions.BasePermission):

    def has_permission(self, request, view):
        user_request = request.user
        data = request.data.get('user')

        user = get_object_or_404(User,phone=user_request.phone)
        return user.id == data