from django.contrib.auth.models import User
from django.db import models
from django.core import validators
from django_countries.fields import CountryField


class Flight(models.Model):

    flight_code = models.CharField(max_length=8, unique=True)

    origin_country = CountryField()
    origin_city = models.CharField(max_length=36)
    origin_airport_code = models.CharField(max_length=16)

    dest_country = CountryField()
    dest_city = models.CharField(max_length=36)
    dest_airport_code = models.CharField(max_length=16)

    departure_dt = models.DateTimeField()
    arrival_dt = models.DateTimeField()

    total_seats = models.IntegerField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(700)])
    seats_left = models.IntegerField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(700)])
    price = models.FloatField(validators=[validators.MinValueValidator(0)])

    is_cancelled = models.BooleanField(default=False)

    class Meta:
        db_table = 'flights'
        ordering = ['id']

# class OrderUsers:
#     pass

class Order(models.Model):

    flight = models.ForeignKey(Flight, on_delete=models.RESTRICT, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='orders')

    # users = models.ManyToManyField(User, through=OrderUsers, related_name='orders')

    seats = models.IntegerField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(700)])
    order_date = models.DateField(auto_now_add=True)
    total_price = models.FloatField(validators=[validators.MinValueValidator(0)], blank=True, null=False)

    class Meta:
        db_table = 'orders'
        ordering = ['id']
