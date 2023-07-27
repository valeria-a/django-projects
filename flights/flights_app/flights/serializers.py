from rest_framework import serializers

from flights_app import models


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Flight
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        validated_data['created_by'] = user
        return super().create(validated_data)
