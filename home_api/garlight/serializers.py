from garlight.models import Color, Temperature, Timer, YeelightBulb
from rest_framework.serializers import ModelSerializer


class BulbSerializer(ModelSerializer):
    class Meta:
        model = YeelightBulb
        fields = "__all__"
        read_only_fields = ("bulb_id", "ip")


class NameSerializer(ModelSerializer):
    class Meta:
        model = YeelightBulb
        fields = ("name",)


class TemperatureSerializer(ModelSerializer):
    class Meta:
        model = Temperature
        fields = "__all__"


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class TimerSerializer(ModelSerializer):
    class Meta:
        model = Timer
        fields = "__all__"
