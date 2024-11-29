from django.urls import path

from .views import LoginView, LogoutView, TokenView

auth_urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/", TokenView.as_view(), name="token"),
]
