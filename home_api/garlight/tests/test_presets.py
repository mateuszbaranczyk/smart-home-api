from django.test import TestCase

from garlight.models import Brightness, Color, Temperature, Timer, presets


class PresetsTest(TestCase):
    def test_presets(self):
        Color.objects.create(
            name="test_color", r=255, g=255, b=255, brightness=100
        )
        Temperature.objects.create(
            name="test_temperature", kelvins=2000, brightness=100
        )
        Timer.objects.create(minutes=1)
        Brightness.objects.create(name="test_brightness", brightness=100)
        result = presets()
        assert result == {
            "power": "Power",
            "test_color": "Color - test_color",
            "test_temperature": "Temperature - test_temperature",
            "1": "Timer - 1",
            "test_brightness": "Brightness - test_brightness",
        }
