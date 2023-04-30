from rest_framework.routers import DefaultRouter

from flights_app.orders.views import OrdersViewSet

router = DefaultRouter()
router.register('', OrdersViewSet)

urlpatterns = router.urls
