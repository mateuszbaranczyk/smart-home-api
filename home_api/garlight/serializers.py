from garlight.models import Color, Endpoint, Temperature, Timer, YeelightBulb
from rest_framework.serializers import ModelSerializer, IntegerField, CharField


class BulbSerializer(ModelSerializer):
    class Meta:
        model = YeelightBulb
        fields = "__all__"
        read_only_fields = ("bulb_id", "ip")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        urls = self.context.get("urls", None)
        if urls:
            representation["urls"] = urls[instance.name]
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


class EndpointSerializer(ModelSerializer):
    name = CharField(max_length=32)
    action = CharField(max_length=16)
    device = CharField(max_length=16)
    preset = CharField(max_length=16)

    def validate(self, data):
        if data["action"] == "on-off":
            if data["preset"] != "":
                raise ValueError("Power action does not require a preset")
        if data["action"] == "color":
            if data["preset"] == "":
                raise ValueError("Color action requires a preset")
        if data["action"] == "temperature":
            if data["preset"] == "":
                raise ValueError("Temperature action requires a preset")
        if data["action"] == "timer":
            if data["preset"] == "":
                raise ValueError("Timer action requires a preset")

    class Meta:
        model = Endpoint
        fields = "__all__"
