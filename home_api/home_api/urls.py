from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from garlight.views import BulbViewSet, ColorViewSet, PowerViewSet

router = DefaultRouter()
router.register(r"bulbs", BulbViewSet, basename="bulbs")
router.register(r"on-off", PowerViewSet, basename="power")
router.register(r"color", ColorViewSet, basename="color")
router.register(r"temperature", ColorViewSet, basename="temperature")

urlpatterns = [
    path("admin/", admin.site.urls),
] + router.urls
