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
            "remember_me": False,
        }
        User.objects.create_user(
            username=data["username"], password=data["password"]
        )
        response = self.client.post(reverse("login"), data)
        assert response.status_code == 302

    def test_logout(self):
        response = self.client.get(reverse("logout"))
        assert response.status_code == 302
