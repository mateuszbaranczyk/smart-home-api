from django.contrib import admin
from django.urls import path
from garlight import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"bulbs", views.BulbViewSet, basename="bulb")
router.register(r"on-off", views.BulbPowerViewSet, basename="bulb-power")
router.register(r"color", views.BulbColorViewSet, basename="bulb-color")
router.register(r"temperature", views.BulbTemperatureViewSet, basename="bulb-temp")
router.register(r"timer", views.BulbTimerViewSet, basename="bulb-timer")
router.register(r"endpoint", views.EndpointViewSet, basename="bulb-endpoint")

router.register(r"colors", views.ColorViewSet, basename="colors")
router.register(r"temperatures", views.TemperatureViewSet, basename="temperatures")
router.register(r"timers", views.TimerViewSet, basename="timers")
router.register(r"endpoints", views.GarminEndpointsViewSet, basename="garmin-endpoints")

urlpatterns = [
    path("admin/", admin.site.urls),
] + router.urls
