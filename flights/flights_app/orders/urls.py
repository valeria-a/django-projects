from rest_framework.routers import DefaultRouter

from flights_app.orders.views import OrdersViewSet, calc_sum

from django.urls import path

router = DefaultRouter()
router.register('', OrdersViewSet)

urlpatterns = [
    path('calc', calc_sum)
]

urlpatterns.extend(router.urls)
