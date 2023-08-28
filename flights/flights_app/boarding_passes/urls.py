from django.urls import path
from rest_framework.routers import DefaultRouter

from flights_app.boarding_passes.views import BoardigPassesViewSet, download_boarding_pass

router = DefaultRouter()
router.register('', BoardigPassesViewSet)

urlpatterns = router.urls
urlpatterns.extend([
    path('download', download_boarding_pass)
])