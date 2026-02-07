from rest_framework.permissions import BasePermission

class IsRebeccaOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.username
            and request.user.username.lower() == "rebecca"
        )
