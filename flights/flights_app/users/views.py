from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet

from flights_app.users.serializers import UserSerializer


class UsersViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()