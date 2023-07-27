from django.contrib.auth.models import User
from django.db import models
from django.core import validators
from django_countries.fields import CountryField

# User <-> Profile
# u: User
# u.profile_set[0]
# u.profile

# ForeignKey -> One2Many
# ManyToMany
# OneToOne

#user: User => user.profile

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.RESTRICT, related_name='profile')
    # user = models.ForeignKey(
    #     User, on_delete=models.RESTRICT, related_name='profile')
    address = models.CharField(max_length=256, null=True)

    img_url = models.CharField(max_length=1024, null=True)

    class Meta:
        db_table = 'profiles'

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

    total_seats = models.IntegerField(
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(700)])
    seats_left = models.IntegerField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(700)])
    price = models.FloatField(validators=[validators.MinValueValidator(0)])

    is_cancelled = models.BooleanField(default=False)

    class Meta:
        db_table = 'flights'
        ordering = ['id']

# o = Order()
# o.flight => Flight => o.flight.seats_left => o.flight.id
# o.flight_id => int

class Order(models.Model):

    flight = models.ForeignKey(Flight, on_delete=models.RESTRICT, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='orders')

    seats = models.IntegerField(
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(700)])
    order_date = models.DateField(auto_now_add=True)
    total_price = models.FloatField(validators=[validators.MinValueValidator(0)], blank=True, null=False)

    class Meta:
        db_table = 'orders'
        ordering = ['id']
