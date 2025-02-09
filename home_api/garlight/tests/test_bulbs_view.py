from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.permissions import AllowAny

from garlight.models import Endpoint, YeelightBulb


class BulbsViewTest(TestCase):
    def setUp(self):
        patch(
            "authentication.views.Auth.permission_classes", [AllowAny]
        ).start()

    def tearDown(self):
        patch.stopall()

    def test_create_bulb_not_allowed(self):
        data = {"test": "test"}
        response = self.client.post(reverse("bulb-list"), data)
        assert response.status_code == 405

    def test_list_bulbs(self):
        bulb_data = {"name": "test_bulb", "ip": "1.1.1.1", "bulb_id": "1"}
        YeelightBulb.objects.create(**bulb_data)
        response = self.client.get(reverse("bulb-list"))
        bulb = YeelightBulb.objects.get(name=bulb_data["name"])
        assert response.status_code == 200
        assert response.json()[0]["name"] == bulb.name

    def test_get_bulb_by_name(self):
        bulb_data = {"name": "test_bulb", "ip": "1.1.1.1", "bulb_id": "1"}
        YeelightBulb.objects.create(**bulb_data)
        response = self.client.get(
            reverse("bulb-detail", args=[bulb_data["name"]])
        )
        assert response.status_code == 200
        assert response.json()["name"] == bulb_data["name"]

    def test_update_bulb(self):
        bulb_data = {"name": "test_bulb", "ip": "1.1.1.1", "bulb_id": "1"}
        YeelightBulb.objects.create(**bulb_data)
        new_data = {"name": "new_name"}
        response = self.client.put(
            reverse("bulb-detail", args=[bulb_data["name"]]),
            new_data,
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.json()["name"] == new_data["name"]

    @patch("garlight.views.bulb_actions.discover_bulbs")
    def test_discover_and_assign_bulb(self, mock):
        discovery_result = [
            {
                "ip": "1.1.1.1",
                "port": 55443,
                "capabilities": {
                    "id": "test",
                    "model": "color",
                    "fw_ver": "65",
                    "support": "set_default",
                    "power": "on",
                    "bright": "100",
                    "color_mode": "2",
                    "ct": "2000",
                    "rgb": "10052090",
                    "hue": "262",
                    "sat": "61",
                    "name": "",
                },
            }
        ]
        mock.return_value = discovery_result
        bulb_id = discovery_result[0]["capabilities"]["id"]
        response = self.client.get("/bulbs/discover/")
        result = YeelightBulb.objects.get(bulb_id=bulb_id)
        assert response.status_code == 302
        assert result.name == bulb_id

    def test_bulbs_contains_action_urls(self):
        bulb_data = {"name": "test_bulb", "ip": "1.1.1.1", "bulb_id": "1"}
        expected_value = f"/on-off/{bulb_data["name"]}/?"
        device = YeelightBulb.objects.create(**bulb_data)
        Endpoint.objects.create(
            name="test", device=device, action="on-off", preset=""
        )

        response = self.client.get(
            reverse("bulb-detail", args=[bulb_data["name"]])
        )

        assert response.status_code == 200
        assert response.json()["urls"][0] == expected_value
