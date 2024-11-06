from collections.abc import KeysView

from garlight.models import (
    Brightness,
    Color,
    Endpoint,
    Temperature,
    Timer,
    YeelightBulb,
    presets,
)
from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    ValidationError,
)


class BulbSerializer(ModelSerializer):
    class Meta:
        model = YeelightBulb
        fields = "__all__"
        read_only_fields = ("bulb_id", "ip")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        urls = self.context.get("urls", None)
        if urls:
            representation["urls"] = [
                action.path for action in urls.filter(device_id=instance.id)
            ]
        return representation


class NameSerializer(ModelSerializer):
    class Meta:
        model = YeelightBulb
        fields = ("name",)


class TemperatureSerializer(ModelSerializer):
    kelvins = IntegerField(max_value=6500, min_value=1700)
    brightness = IntegerField(max_value=100, min_value=1)

    class Meta:
        model = Temperature
        fields = "__all__"


class ColorSerializer(ModelSerializer):
    r = IntegerField(max_value=255, min_value=0)
    g = IntegerField(max_value=255, min_value=0)
    b = IntegerField(max_value=255, min_value=0)
    brightness = IntegerField(max_value=100, min_value=1)

    class Meta:
        model = Color
        fields = "__all__"


class TimerSerializer(ModelSerializer):
    class Meta:
        model = Timer
        fields = "__all__"


class BrightnessSerializer(ModelSerializer):
    brightness = IntegerField(max_value=100, min_value=1)

    class Meta:
        model = Brightness
        fields = "__all__"


class EndpointSerializer(ModelSerializer):
    def validate(self, attrs):
        all_presets = presets()
        action = attrs["action"]
        action_presets = self._filter_presets(all_presets, action)

        if attrs["action"] == "on-off":
            attrs["preset"] = ""
            return attrs

        if attrs["preset"] not in action_presets:
            raise ValidationError(f"Use preset for {action.capitalize()}")

        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation["name"] == "" and representation["preset"] == "":
            representation["name"] = "Power"
        elif representation["name"] == "":
            representation["name"] = representation["preset"]
        return representation

    def _filter_presets(self, presets: dict, action: str) -> KeysView:
        filtered = {
            key: value
            for key, value in presets.items()
            if action.capitalize() in value
        }
        return filtered.keys()

    class Meta:
        model = Endpoint
        fields = "__all__"
