from django.urls import path, include
from rest_framework.routers import DefaultRouter


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from flights_app.users.views import UsersViewSet, me, ExtendedTokenObtainPairView, google_login

router = DefaultRouter()
router.register('', UsersViewSet)


urlpatterns = [
    # path('tokens', TokenObtainPairView.as_view()),
    path('tokens', ExtendedTokenObtainPairView.as_view()),
    path('tokens/refresh', TokenRefreshView.as_view()),
    path('me', me),
    path('google-auth', google_login)
]
urlpatterns.extend(router.urls)