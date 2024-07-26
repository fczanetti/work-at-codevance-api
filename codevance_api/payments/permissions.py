from rest_framework import permissions


class RequestPermission(permissions.BasePermission):
    """
    Global permission to block requests from users
    that are neither suppliers nor operators.
    """
    message = 'Only suppliers or operators can make requests.'

    def has_permission(self, request, view):
        user = request.user
        if user.is_operator or hasattr(user, 'supplier'):
            return True
        return False
