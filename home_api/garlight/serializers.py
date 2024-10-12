from rest_framework.serializers import ModelSerializer

from garlight.models import Color, Temperature, Timer, YeelightBulb


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
