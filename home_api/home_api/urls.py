from django.contrib import admin
from django.urls import path
from garlight.views import (
    BulbViewSet,
    BulbColorViewSet,
    BulbPowerViewSet,
    BulbTemperatureViewSet,
    ColorViewSet,
    TemperatureViewSet,
    TimerViewSet,
    BulbTimerViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"bulbs", BulbViewSet, basename="bulbs")
router.register(r"on-off", BulbPowerViewSet, basename="bulb-power")
router.register(r"color", BulbColorViewSet, basename="bulb-color")
router.register(
    r"temperature", BulbTemperatureViewSet, basename="bulb-temperature"
)
router.register("timer", BulbTimerViewSet, basename="bulb-timer")

router.register(r"colors", ColorViewSet, basename="colors")
router.register(r"temperatures", TemperatureViewSet, basename="temperatures")
router.register(r"timers", TimerViewSet, basename="timers")

urlpatterns = [
    path("admin/", admin.site.urls),
] + router.urls
