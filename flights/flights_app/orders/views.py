from django.http import JsonResponse
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from flights_app.orders import serializers
from flights_app import models
from flights_app.orders.permissions import OrdersPermission


class OrdersViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.all()
    permission_classes = [IsAuthenticated, OrdersPermission]


@api_view(['GET'])
def calc_sum(request):
    num1 = request.GET.get('num1')
    num2 = request.GET.get('num2')

    # validate

    res = int(num1) + int(num2)
    return JsonResponse({'result': res})
