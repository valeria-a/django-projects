from rest_framework.permissions import BasePermission, SAFE_METHODS


class OrdersPermission(BasePermission):

    # Called for all the types of action - list, create, retrieve, destroy, update
    def has_permission(self, request, view):
        # methods of list, create reach this code
        if view.action == 'list':
            return request.user.is_staff
        return True

    # called only for object-specific actions: retrieve, destroy, update
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve' or view.action == 'update':
            return request.user.is_staff or request.user == obj.user