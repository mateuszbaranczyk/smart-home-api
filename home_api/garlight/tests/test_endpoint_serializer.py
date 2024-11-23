from django.test import TestCase
from rest_framework.exceptions import ErrorDetail

from garlight.models import Brightness, Color, YeelightBulb
from garlight.serializers import EndpointSerializer


class EndpointSerializerTest(TestCase):
    def setUp(self):
        self.brightness = Brightness.objects.create(
            name="full", brightness=100
        )
        self.color = Color.objects.create(
            name="test_color", r=255, g=255, b=255, brightness=100
        )
        self.bulb = YeelightBulb.objects.create(
            name="test_bulb", ip="1.1.1.1.1", bulb_id="xxxtest123"
        )
        self.form_data = {
            "name": "Test Endpoint",
            "action": "color",
            "preset": self.color.name,
            "device": self.bulb.id,
        }

    def test_validate_presets(self):
        serializer = EndpointSerializer(data=self.form_data)
        is_valid = serializer.is_valid()
        data = serializer.validated_data
        assert is_valid is True
        assert data["name"] == "Test Endpoint"
        assert data["action"] == "color"
        assert data["preset"] == self.color.name
        assert data["device"] == self.bulb

    def test_returns_empty_preset_on_power_action(self):
        self.form_data["action"] = "on-off"
        serializer = EndpointSerializer(data=self.form_data)
        serializer.is_valid()
        data = serializer.validated_data
        assert data["preset"] == ""

    def test_raise_error_on_incorrect_preset(self):
        self.form_data["preset"] = "full"
        serializer = EndpointSerializer(data=self.form_data)
        is_valid = serializer.is_valid()
        assert is_valid is False
        assert serializer.errors["non_field_errors"][0] == ErrorDetail(
            string="Use preset for Color", code="invalid"
        )

    def test_to_representation(self):
        serializer = EndpointSerializer(data=self.form_data)
        serializer.is_valid()
        instance = serializer.save()
        representation = serializer.to_representation(instance)
        assert representation["name"] == self.form_data["name"]
        assert representation["action"] == self.form_data["action"]
        assert representation["device"] == self.bulb.id
        assert representation["preset"] == self.color.name

    def test_auto_name_for_power(self):
        serializer = EndpointSerializer(data=self.form_data)
        serializer.is_valid()
        instance = serializer.save()
        instance.name = ""
        instance.preset = ""
        representation = serializer.to_representation(instance)
        assert representation["name"] == "Power"

    def test_auto_set_name(self):
        serializer = EndpointSerializer(data=self.form_data)
        serializer.is_valid()
        instance = serializer.save()
        instance.name = ""
        representation = serializer.to_representation(instance)
        assert representation["name"] == self.form_data["preset"]