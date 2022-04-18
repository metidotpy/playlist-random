from rest_framework import permissions

class IsAnonymous(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user.is_anonymous or request.user.is_staff or request.user.is_superuser)
