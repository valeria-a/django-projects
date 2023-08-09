import django_filters
from django.db.models import Q

from flights_app.models import Flight


class FlightsFilterSet(django_filters.FilterSet):

    flight_code = django_filters.CharFilter(lookup_expr='iexact')
    origin = django_filters.CharFilter(method='origin_filter')
    origin_city = django_filters.CharFilter(field_name='origin_city', lookup_expr='iexact')
    dest = django_filters.CharFilter(method='dest_filter')
    departure = django_filters.DateFromToRangeFilter(field_name='departure_dt')
    arrival = django_filters.DateFromToRangeFilter(field_name='arrival_dt')
    price = django_filters.RangeFilter(field_name='price')
    cancelled = django_filters.BooleanFilter(field_name='is_cancelled')

    # origin='new york'
    def origin_filter(self, queryset, name, value):
        queryset = queryset.filter(Q(origin_country__iexact=value) |
                                   Q(origin_city__icontains=value) |
                                   Q(origin_airport_code__iexact=value))
        return queryset

    def dest_filter(self, queryset, name, value):
        queryset = queryset.filter(Q(dest_country__iexact=value) |
                                   Q(dest_city__icontains=value) |
                                   Q(dest_airport_code__iexact=value))
        return queryset

    class Meta:
        model = Flight
        fields = []