from unittest.mock import patch

from django.urls import reverse
from garlight.models import Color
from pytest import fixture
from rest_framework.permissions import AllowAny


@fixture(autouse=True)
def set_up():
    with patch("authentication.views.Auth.permission_classes", [AllowAny]):
        yield

def test_create_color(client, db):
    color_data = {
        "name": "test_color",
        "brightness": 1,
        "r": 1,
        "g": 1,
        "b": 1,
    }
    response = client.post(reverse("colors-list"), color_data)
    result = Color.objects.get(name=color_data["name"])
    assert response.status_code == 201
    assert result.name == color_data["name"]


def test_list_colors(client, db):
    color_data = {
        "name": "test_color",
        "brightness": 1,
        "r": 1,
        "g": 1,
        "b": 1,
    }
    Color.objects.create(**color_data)
    response = client.get(reverse("colors-list"))
    assert response.status_code == 200
    assert response.data[0]["name"] == color_data["name"]


def test_retrieve_color(client, db):
    color_data = {
        "name": "test_color",
        "brightness": 1,
        "r": 1,
        "g": 1,
        "b": 1,
    }
    color = Color.objects.create(**color_data)
    response = client.get(reverse("colors-detail", args=[color.id]))
    assert response.status_code == 200
    assert response.data["name"] == color_data["name"]
