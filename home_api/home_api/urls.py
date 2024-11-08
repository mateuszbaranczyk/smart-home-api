from authentication.urls import urlpatterns as authentication_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from garlight.urls import garlight_urls

urlpatterns = (
    [
        path("admin/", admin.site.urls),
    ]
    + garlight_urls
    + authentication_urls
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
