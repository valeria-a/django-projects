from django.http import JsonResponse
from rest_framework.decorators import api_view, action
from rest_framework.viewsets import ModelViewSet

from flights_app.flights import serializers
from flights_app import models
from flights_app.flights.filters import FlightsFilterSet
from flights_app.flights.permissions import FlightsPermission
from flights_app.models import Flight
from rest_framework.response import Response


class FlightsViewSet(ModelViewSet):

    serializer_class = serializers.FlightSerializer
    queryset = models.Flight.objects.all()
    filterset_class = FlightsFilterSet
    permission_classes = (FlightsPermission, )

    @action(['GET'],detail=False)
    def stats(self):
        self.get_queryset()


@api_view(['GET'])
def get_origin_cities(request):
    all_origins = list(Flight.objects.order_by().values_list('origin_city').distinct())
    all_origins = [city for sublist in all_origins for city in sublist]
    # my_list = [1,2,3,4]
    # new_list = [num+1 for num in my_list]
    # ret_list = []
    # for sublist in all_origins:
    #     for city in sublist:
    #         ret_list.append(city)
    print(all_origins)
    return JsonResponse(data=list(all_origins), safe=False)
