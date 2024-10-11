from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'SUPER_ADMIN'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['SUPER_ADMIN', 'ADMIN','PLAYER']

class IsCoach(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['SUPER_ADMIN', 'ADMIN', 'COACH']