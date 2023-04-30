from django.urls import path
from rest_framework.routers import DefaultRouter

from flights_app.flights.views import FlightsViewSet

router = DefaultRouter()
router.register('', FlightsViewSet)

urlpatterns = router.urls
