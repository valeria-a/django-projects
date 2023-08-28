from django.urls import path, include
from rest_framework.routers import DefaultRouter


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from flights_app.users.views import UsersViewSet, me, ExtendedTokenObtainPairView, google_login, upload_profile_img, \
    upload_profile_img_url, upload_profile_img_done, download_file

router = DefaultRouter()
router.register('', UsersViewSet)


urlpatterns = [
    # LOGIN
    # path('tokens', TokenObtainPairView.as_view()),
    path('tokens', ExtendedTokenObtainPairView.as_view()),
    path('tokens/refresh', TokenRefreshView.as_view()),
    path('me', me),
    path('google-auth', google_login),
    path('profile/img', upload_profile_img),
    path('profile/img/presigned', upload_profile_img_url),
    path('profile/img/done', upload_profile_img_done),
    path('download', download_file),

]
urlpatterns.extend(router.urls)