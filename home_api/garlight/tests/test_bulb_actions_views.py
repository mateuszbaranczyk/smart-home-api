from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.permissions import AllowAny

from garlight.models import Brightness, Color, Temperature, Timer, YeelightBulb


class ActionsMixin(TestCase):
    def setUp(self):
        self.bulb = YeelightBulb.objects.create(
            bulb_id="bulb_id",
            ip="1.1.1.1.",
            name="bulb_name",
        )
        patch(
            "authentication.views.GarminAuth.permission_classes", [AllowAny]
        ).start()

    def tearDown(self):
        patch.stopall()

class YeelightViewSetTest(ActionsMixin):
    def setUp(self):
        super().setUp()
        self.url = reverse("bulb-color-detail", args=[self.bulb.name])
        patch(
            "garlight.bulbs.SmartBulb.set_color", return_value="test"
        ).start()
        self.color = Color(
            name="test_color", r=255, g=255, b=255, brightness=100
        )

    def test_raise_error_on_missing_param(self):
        response = self.client.get(self.url)
        assert response.status_code == 404
        assert response.content == b'{"detail":"Query keys not found"}'


class PowerTest(ActionsMixin):
    def setUp(self):
        super().setUp()
        self.url = f"/on-off/{self.bulb.name}/"
        patch("garlight.bulbs.SmartBulb.on_off", return_value="test").start()

    def test_power(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.headers._store["content-type"][1] == "text/plain"


class ColorTest(ActionsMixin):
    def setUp(self):
        super().setUp()
        self.url = f"/color/{self.bulb.name}/"
        patch(
            "garlight.bulbs.SmartBulb.set_color", return_value="test"
        ).start()
        self.color = Color(
            name="test_color", r=255, g=255, b=255, brightness=100
        )

    def test_color(self):
        self.url += f"?{self.color.name}"
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.headers._store["content-type"][1] == "text/plain"


class TemperatureTest(ActionsMixin):
    def setUp(self):
        super().setUp()
        self.url = reverse("bulb-temp-detail", args=[self.bulb.name])
        patch(
            "garlight.bulbs.SmartBulb.set_temperature", return_value="test"
        ).start()
        self.temperature = Temperature(
            name="test_temperature", kelvins=100, brightness=100
        )

    def test_temperature(self):
        self.url += f"?{self.temperature.name}"
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.headers._store["content-type"][1] == "text/plain"


class TimerTest(ActionsMixin):
    def setUp(self):
        super().setUp()
        self.url = reverse("bulb-timer-detail", args=[self.bulb.name])
        patch(
            "garlight.bulbs.SmartBulb.set_timer", return_value="test"
        ).start()
        self.timer = Timer.objects.create(minutes=1)

    def test_timer(self):
        self.url += "?1"
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.headers._store["content-type"][1] == "text/plain"


class BrightnessTest(ActionsMixin):
    def setUp(self):
        super().setUp()
        self.url = reverse("bulb-brightness-detail", args=[self.bulb.name])
        patch(
            "garlight.bulbs.SmartBulb.set_brightness", return_value="test"
        ).start()
        self.brightness = Brightness.objects.create(
            name="test_brightness", brightness=100
        )
    
    def test_brightness(self):
        self.url += f"?{self.brightness.name}"
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.headers._store["content-type"][1] == "text/plain"
