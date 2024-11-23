from unittest.mock import patch

from django.test import SimpleTestCase

from garlight.bulbs import SmartBulb
from garlight.models import Color, Temperature, YeelightBulb

DISCOVERY = {
    "ip": "1.1.1.1",
    "port": 55443,
    "power": "on",
    "capabilities": {
        "id": "test",
        "model": "color",
        "fw_ver": "65",
        "support": "set_default",
        "bright": "100",
        "color_mode": "2",
        "ct": "2000",
        "rgb": "10052090",
        "hue": "262",
        "sat": "61",
        "name": "",
    },
}


class SmartBulbTestCase(SimpleTestCase):
    # Useless for now but can be useful in the future refactoring
    def setUp(self):
        yeelight = YeelightBulb(name="Test", ip="1.1.1.1", bulb_id="xxtest123")
        self.smart_bulb = SmartBulb(yeelight)

    def tearDown(self):
        patch.stopall()

    def test_power_on(self):
        patch(
            "garlight.bulbs.Bulb.get_capabilities",
            return_value={"power": "off"},
        ).start()
        patch("garlight.bulbs.Bulb.turn_on", return_value=None).start()
        result = self.smart_bulb.on_off()
        self.assertEqual(result, "Power on")

    def test_power_off(self):
        patch(
            "garlight.bulbs.Bulb.get_capabilities",
            return_value={"power": "on"},
        ).start()
        patch("garlight.bulbs.Bulb.turn_off", return_value=None).start()
        result = self.smart_bulb.on_off()
        self.assertEqual(result, "Power off")

    def test_set_timer(self):
        patch("garlight.bulbs.Bulb.cron_add", return_value="ok").start()
        assert self.smart_bulb.set_timer(15) == "Timer to 15 min."

    def test_timer_error_msg(self):
        patch("garlight.bulbs.Bulb.cron_add", return_value="error").start()
        assert self.smart_bulb.set_timer(15) == "Failed"

    def test_set_color(self):
        patch("garlight.bulbs.Bulb.set_scene", return_value="ok").start()
        color = Color("test", brightness=100, r=255, g=255, b=255)
        assert self.smart_bulb.set_color(color) == "Ok"

    def test_set_temperature(self):
        patch("garlight.bulbs.Bulb.set_scene", return_value="ok").start()
        temperature = Temperature("test", brightness=100, kelvins=2000)
        assert self.smart_bulb.set_temperature(temperature) == "Ok"

    def test_set_brightness(self):
        patch("garlight.bulbs.Bulb.set_brightness", return_value="ok").start()
        assert self.smart_bulb.set_brightness(100) == "Ok"

    def test_set_brightness_on_turned_off(self):
        patch(
            "garlight.bulbs.Bulb.get_capabilities",
            return_value={"power": "off"},
        ).start()
        patch("garlight.bulbs.Bulb.turn_on", return_value=None).start()
        patch("garlight.bulbs.Bulb.set_brightness", return_value="ok").start()
        assert self.smart_bulb.set_brightness(100) == "Ok"
