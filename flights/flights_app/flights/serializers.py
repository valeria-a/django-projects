from rest_framework import serializers

from flights_app import models


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Flight
        fields = '__all__'
