from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner.email == request.user.email


class IsSameUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.email == request.data.get("email")
