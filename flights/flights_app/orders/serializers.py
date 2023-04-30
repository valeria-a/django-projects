from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from flights_app import models
from flights_app.models import Flight, Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = '__all__'

    def create(self, validated_data):
        with transaction.atomic():
            flight = Flight.objects.select_for_update().get(id=validated_data['flight'].id)
            if flight.seats_left < validated_data['seats']:
                raise ValidationError(detail='Not enough seats')

            # calculate total price before storing new order
            total_price = flight.price * validated_data['seats']
            order = Order.objects.create(total_price=total_price, **validated_data)

            # update seats left in flight
            flight.seats_left = flight.seats_left - validated_data['seats']
            flight.save()

            return order

    def update(self, instance, validated_data):
        old_flight_id = instance.flight.id
        new_flight_id = validated_data['flight'].id if 'flight' in validated_data else old_flight_id
        old_seats = instance.seats
        new_seats = validated_data['seats'] if 'seats' in validated_data else old_seats
        with transaction.atomic():
            order = Order.objects.select_for_update().get(id=instance.id)
            old_flight = Flight.objects.select_for_update().get(id=old_flight_id)
            if old_flight_id == new_flight_id:
                new_flight = old_flight
            else:
                new_flight = Flight.objects.select_for_update().get(id=new_flight_id)

            # check seats availability
            if old_flight_id == new_flight_id:
                # the same flight
                if old_seats < new_seats:
                    if new_flight.seats_left < new_seats - old_seats:
                        raise ValidationError('Not enough seats left')
            else:
                # different flights
                if new_flight.seats_left < new_seats:
                    raise ValidationError('Not enough seats left')

            # make all the needed updates
            old_flight.seats_left = old_flight.seats_left + order.seats
            new_flight.seats_left = new_flight.seats_left - validated_data['seats']
            order.seats = validated_data['seats']
            order.total_price = validated_data['seats'] * new_flight.price
            order.flight_id = new_flight_id
            old_flight.save()
            new_flight.save()
            order.save()

        return order

    def validate(self, attrs):
        flight = attrs.get('flight')
        if flight and flight.seats_left < attrs['seats']:
            raise ValidationError(detail='Not enough seats')
        return attrs

