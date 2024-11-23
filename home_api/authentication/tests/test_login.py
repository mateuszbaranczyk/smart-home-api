from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginTest(TestCase):
    def test_get_login_page(self):
        response = self.client.get(reverse("login"))
        assert response.status_code == 200
        assert "username" in response.content.decode()
        assert "password" in response.content.decode()
        assert "remember_me" in response.content.decode()
        assert "Login" in response.content.decode()

    def test_login(self):
        data = {
            "username": "test",
            "password": "password",
            "remember_me": True,
        }
        User.objects.create_user(
            username=data["username"], password=data["password"]
        )
        response = self.client.post(reverse("login"), data)
        assert self.client.session is not None
        assert response.status_code == 302

    def test_logout(self):
        response = self.client.get(reverse("logout"))
        assert response.status_code == 302

    def test_login_failed(self):
        data = {
            "username": "test",
            "password": "password",
            "remember_me": False,
        }
        response = self.client.post(reverse("login"), data)
        assert response.status_code == 400
        assert "Invalid credentials" in response.content.decode()
