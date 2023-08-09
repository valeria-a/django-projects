from django.urls import path
from rest_framework.routers import DefaultRouter

from flights_app.flights.views import FlightsViewSet, get_origin_cities

router = DefaultRouter()
router.register('', FlightsViewSet)

urlpatterns = router.urls

urlpatterns.extend([
    path('origin_cities', get_origin_cities),
])
