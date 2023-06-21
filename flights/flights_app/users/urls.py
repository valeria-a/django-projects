from django.urls import path, include
from rest_framework.routers import DefaultRouter


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from flights_app.users.views import UsersViewSet, me

router = DefaultRouter()
router.register('', UsersViewSet)


urlpatterns = [
    path('tokens', TokenObtainPairView.as_view()),
    path('tokens/refresh', TokenRefreshView.as_view()),
    path('me', me)
]
urlpatterns.extend(router.urls)