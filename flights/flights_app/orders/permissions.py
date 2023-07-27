from rest_framework.permissions import BasePermission, SAFE_METHODS


class OrdersPermission(BasePermission):
    def has_permission(self, request, view):
        # methods of list, create reach this code
        if view.action == 'list':
            return request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve' or view.action == 'update':
            return request.user.is_staff or request.user == obj.user