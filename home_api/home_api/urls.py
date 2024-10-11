from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from garlight.views import BulbViewSet

router = DefaultRouter()
router.register(r"bulbs", BulbViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
] + router.urls
