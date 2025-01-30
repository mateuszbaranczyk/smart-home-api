from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.permissions import AllowAny

from aura.models import Location
from aura.tests.response import eg_forecast_response


class LocationViewSetTest(TestCase):
    def setUp(self):
        patch(
            "authentication.views.Auth.permission_classes", [AllowAny]
        ).start()
        self.location_data = {"name": "test", "lat": 20, "lon": 20}

    def tearDown(self):
        patch.stopall()

    def test_create_location(self):
        response = self.client.post(
            reverse("location-list"), self.location_data
        )
        assert response.status_code == 201
        assert Location.objects.get(name=self.location_data["name"])

    def test_list_locations(self):
        Location.objects.create(**self.location_data)
        response = self.client.get(reverse("location-list"))
        location = Location.objects.get(name=self.location_data["name"])
        assert response.status_code == 200
        assert response.json()[0]["name"] == location.name

    def test_get_location_by_name(self):
        Location.objects.create(**self.location_data)
        response = self.client.get(
            reverse("location-detail", args=[self.location_data["name"]])
        )
        assert response.status_code == 200
        assert response.json()["name"] == self.location_data["name"]


class CurrentWeatherViewTest(TestCase):
    def setUp(self):
        patch(
            "authentication.views.GarminAuth.permission_classes", [AllowAny]
        ).start()
        self.location_data = {"name": "test", "lat": 20, "lon": 20}
        self.location = Location.objects.create(**self.location_data)

    @patch("aura.adapters.requests.get")
    def test_get_current_weather(self, m_requests):
        expected = (
            b"Temp: 0.2 C\nFeel: -5.1 C\nWind: 20.9 km/h\nAir: 3/10\nClear"
        )
        m_requests.return_value.status_code = 200
        m_requests.return_value.json.return_value = eg_forecast_response
        response = self.client.get(
            reverse("current-detail", args=[self.location_data["name"]])
        )
        assert response.status_code == 200
        assert response.content == expected

    @patch("aura.adapters.requests.get")
    def test_get_current_weather_error(self, m_requests):
        m_requests.return_value.status_code = 404
        response = self.client.get(
            reverse("current-detail", args=[self.location_data["name"]])
        )
        assert response.status_code == 200
        assert "Adapter error:" in str(response.content, "utf-8")


class ForecastWeatherViewTest(TestCase):
    def setUp(self):
        patch(
            "authentication.views.GarminAuth.permission_classes", [AllowAny]
        ).start()
        self.location_data = {"name": "test", "lat": 20, "lon": 20}
        self.location = Location.objects.create(**self.location_data)

    @patch("aura.adapters.requests.get")
    def test_get_forecast_weather(self, m_requests):
        expected = b"Temp: 7.3 C\nFeel: 2.5 C\nWind: 37.8 km/h\nCloudy "
        m_requests.return_value.status_code = 200
        m_requests.return_value.json.return_value = eg_forecast_response
        response = self.client.get(
            reverse("forecast-detail", args=[self.location_data["name"]])
        )
        assert response.status_code == 200
        assert response.content == expected

    @patch("aura.adapters.requests.get")
    def test_get_forecast_weather_error(self, m_requests):
        m_requests.return_value.status_code = 404
        response = self.client.get(
            reverse("forecast-detail", args=[self.location_data["name"]])
        )
        assert response.status_code == 200
        assert "Adapter error:" in str(response.content, "utf-8")


class WeatherDefinitionsViewTest(TestCase):
    def setUp(self):
        patch(
            "authentication.views.GarminAuth.permission_classes", [AllowAny]
        ).start()
        self.location_data = {"name": "test", "lat": 20, "lon": 20}
        self.location = Location.objects.create(**self.location_data)

    def tearDown(self):
        patch.stopall()

    def test_get_weather(self):
        expected = b"- all,Yeelight\n-- test,Test (Weather)\n--- current,Current,/current/test\n--- forecast,Forecast,/forecast/test\n-- Test2,Test2 (Weather)\n--- current,Current,/current/Test2\n--- forecast,Forecast,/forecast/Test2\n"
        self.location_data["name"] = "Test2"
        Location.objects.create(**self.location_data)
        response = self.client.get("/endpoints/")
        assert response.status_code == 200
        assert expected in response.content
