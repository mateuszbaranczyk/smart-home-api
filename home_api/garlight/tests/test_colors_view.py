from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.permissions import AllowAny

from garlight.models import Color


class ColorsViewTest(TestCase):
    def setUp(self):
        self.color_data = {
            "name": "test_color",
            "brightness": 1,
            "r": 1,
            "g": 1,
            "b": 1,
        }
        patch(
            "authentication.views.Auth.permission_classes", [AllowAny]
        ).start()

    def test_create_color(self):
        response = self.client.post(reverse("colors-list"), self.color_data)
        result = Color.objects.get(name=self.color_data["name"])
        assert response.status_code == 201
        assert result.name == self.color_data["name"]

    def test_list_colors(self):
        Color.objects.create(**self.color_data)
        response = self.client.get(reverse("colors-list"))
        assert response.status_code == 200
        assert response.data[0]["name"] == self.color_data["name"]

    def test_retrieve_color(self):
        color = Color.objects.create(**self.color_data)
        response = self.client.get(reverse("colors-detail", args=[color.id]))
        assert response.status_code == 200
        assert response.data["name"] == self.color_data["name"]
