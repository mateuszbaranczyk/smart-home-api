from django.contrib.auth.models import User
from django.urls import reverse


def test_get_login_page(client):
    response = client.get(reverse("login"))
    assert response.status_code == 200
    assert "username" in response.content.decode()
    assert "password" in response.content.decode()
    assert "remember_me" in response.content.decode()
    assert "Login" in response.content.decode()


def test_login(client, db):
    data = {
        "username": "test",
        "password": "password",
        "remember_me": False,
    }
    User.objects.create_user(
        username=data["username"], password=data["password"]
    )
    response = client.post(reverse("login"), data)
    assert response.status_code == 302


def test_logout(client):
    response = client.get(reverse("logout"))
    assert response.status_code == 302
