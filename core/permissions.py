from rest_framework.permissions import IsAuthenticated

from .models import BaseUser


class IsEmployee(IsAuthenticated):

    def has_permission(self, request, view):
        return bool(request.user.is_employee and request.user)


class IsIncharge(IsAuthenticated):
    
    def has_permission(self, request, view):
        incharge_user = BaseUser.objects.filter(pk=request.user.id, delete=False, is_employee=True , role__pk=1).exists()
        return bool(incharge_user and request.user)


class IsAdmin(IsAuthenticated):

    def has_permission(self, request, view):
        # admin_user = BaseUser.objects.filter(pk=request.user.id, delete=False, is_staff=True).exists()
        return bool(request.user.is_staff and request.user)


class IsSuperAdmin(IsAuthenticated):

    def has_permission(self, request, view):
        # super_admin_user = BaseUser.objects.filter(pk=request.user.id, delete=False, is_superuser=True, is_staff=True).exists()
        return bool(request.user.is_staff and request.user.is_superuser and request.user)
