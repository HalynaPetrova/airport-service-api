from rest_framework import routers

from airport.views import (
    AirportViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    CrewViewSet,
    FacilityViewSet,
    FlightViewSet,
    OrderViewSet,
    RouteViewSet,
)

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("crews", CrewViewSet)
router.register("facilities", FacilityViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)
router.register("routes", RouteViewSet)

urlpatterns = router.urls
app_name = "airport"
