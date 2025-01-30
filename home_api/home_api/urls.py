from aura.urls import aura_urls
from authentication.urls import auth_urlpatterns as authentication_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from garlight.urls import garlight_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(garlight_urls)),
    path("", include(authentication_urls)),
    path("", include(aura_urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
