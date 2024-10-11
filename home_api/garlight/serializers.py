from garlight.models import YeelightBulb
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
