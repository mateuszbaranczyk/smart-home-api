from django.contrib import admin
from django.urls import path
from garlight.urls import garlight_urls

urlpatterns = [
    path("admin/", admin.site.urls),
] + garlight_urls
