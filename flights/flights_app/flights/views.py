from rest_framework.viewsets import ModelViewSet

from flights_app.flights import serializers
from flights_app import models
from flights_app.flights.filters import FlightsFilterSet
from flights_app.flights.permissions import FlightsPermission


class FlightsViewSet(ModelViewSet):

    serializer_class = serializers.FlightSerializer
    queryset = models.Flight.objects.all()
    filterset_class = FlightsFilterSet
    permission_classes = FlightsPermission
