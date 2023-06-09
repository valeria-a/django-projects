# Generated by Django 4.2 on 2023-04-28 11:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_code', models.CharField(max_length=8, unique=True)),
                ('origin_country', django_countries.fields.CountryField(max_length=2)),
                ('origin_city', models.CharField(max_length=36)),
                ('origin_airport_code', models.CharField(max_length=16)),
                ('dest_country', django_countries.fields.CountryField(max_length=2)),
                ('dest_city', models.CharField(max_length=36)),
                ('dest_airport_code', models.CharField(max_length=16)),
                ('departure_dt', models.DateTimeField()),
                ('arrival_dt', models.DateTimeField()),
                ('total_seats', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(700)])),
                ('seats_left', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(700)])),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('is_cancelled', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'flights',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(700)])),
                ('order_date', models.DateField(auto_now_add=True)),
                ('total_price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='orders', to='flights_app.flight')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
    ]
