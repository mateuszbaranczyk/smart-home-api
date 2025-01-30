from unittest.mock import patch

from django.test import TestCase
from rest_framework.permissions import AllowAny

from garlight.models import Color, Endpoint, YeelightBulb


class DefinitionsTest(TestCase):
    def setUp(self):
        patch(
            "authentication.views.GarminAuth.permission_classes", [AllowAny]
        ).start()

    def tearDown(self):
        patch.stopall()

    def test_get_endpoints(self):
        expected_result = b"- all,Yeelight\n-- test_bulb,Test_bulb\n--- color,Color\n---- test_endpoint,Test_endpoint,/color/test_bulb/?test_color\n"
        bulb = YeelightBulb.objects.create(
            name="test_bulb", ip="1.1.1.1", bulb_id="1"
        )
        Color.objects.create(
            name="test_color", r=255, g=255, b=255, brightness=100
        )
        Endpoint.objects.create(
            name="test_endpoint",
            action="color",
            preset="test_color",
            device=bulb,
        )
        response = self.client.get("/endpoints/")
        assert response.status_code == 200
        assert expected_result in response.content
