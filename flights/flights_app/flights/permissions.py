from rest_framework.permissions import BasePermission, SAFE_METHODS


class FlightsPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user and request.user.is_staff