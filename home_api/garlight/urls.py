from django.urls import include, path
from rest_framework.routers import DefaultRouter

from garlight import views

app_router = DefaultRouter()  # management
device_router = DefaultRouter()  # api for sending requests to devices

# fmt: off
app_router.register(r"bulbs", views.BulbViewSet, basename="bulb")
app_router.register(r"colors", views.ColorViewSet, basename="colors")
app_router.register(r"temperatures", views.TemperatureViewSet, basename="temperatures")
app_router.register(r"timers", views.TimerViewSet, basename="timers")
app_router.register(r"brightnesses", views.BrightnessViewSet, basename="brightnesses")
app_router.register(r"endpoint", views.EndpointViewSet, basename="bulb-endpoint")

device_router.register(r"on-off", views.BulbPowerViewSet, basename="bulb-power")
device_router.register(r"color", views.BulbColorViewSet, basename="bulb-color")
device_router.register(r"temperature", views.BulbTemperatureViewSet, basename="bulb-temp")
device_router.register(r"timer", views.BulbTimerViewSet, basename="bulb-timer")
device_router.register(r"brightness", views.BulbBrightnessViewSet, basename="bulb-brightness")
device_router.register(r"endpoints", views.GarminEndpointsViewSet, basename="bulb-endpoints")
# fmt: on

garlight_urls = [
    path("", include(app_router.urls)),
    path("", include(device_router.urls)),
]
