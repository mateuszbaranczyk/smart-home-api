from django.urls import include, path
from rest_framework.routers import DefaultRouter

from aura.views import CurrentWeatherView, ForecastWeatherView, LocationViewSet

aura_router = DefaultRouter()

aura_router.register(r"location", LocationViewSet, basename="location")
aura_router.register(r"current", CurrentWeatherView, basename="current")
aura_router.register(r"forecast", ForecastWeatherView, basename="forecast")

aura_urls = [
    path("", include(aura_router.urls)),
]