from garlight import views
from rest_framework.routers import DefaultRouter

app_router = DefaultRouter()  # management
device_router = DefaultRouter()  # api for sending requests to devices

# fmt: off
app_router.register(r"bulbs", views.BulbViewSet, basename="bulb")
app_router.register(r"on-off", views.BulbPowerViewSet, basename="bulb-power")
app_router.register(r"color", views.BulbColorViewSet, basename="bulb-color")
app_router.register(r"temperature", views.BulbTemperatureViewSet, basename="bulb-temp")
app_router.register(r"timer", views.BulbTimerViewSet, basename="bulb-timer")
app_router.register(r"brightness", views.BrightnessViewSet, basename="bulb-brightness")
app_router.register(r"endpoint", views.EndpointViewSet, basename="bulb-endpoint")

device_router.register(r"colors", views.ColorViewSet, basename="colors")
device_router.register(r"temperatures", views.TemperatureViewSet, basename="temperatures")
device_router.register(r"timers", views.TimerViewSet, basename="timers")
device_router.register(r"endpoints", views.GarminEndpointsViewSet, basename="endpoints")
# fmt: on

garlight_urls = app_router.urls + device_router.urls
