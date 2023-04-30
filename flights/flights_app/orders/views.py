from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from flights_app.orders import serializers
from flights_app import models
from flights_app.orders.permissions import OrdersPermission


class OrdersViewSet(ModelViewSet):

    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.all()
    permission_classes = [IsAuthenticated, OrdersPermission]
