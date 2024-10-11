from rest_framework.serializers import (
    ModelSerializer,
    BaseSerializer,
    CharField,
)

from garlight.models import YeelightBulb


class BulbSerializer(ModelSerializer):
    class Meta:
        model = YeelightBulb
        fields = "__all__"
        read_only_fields = ("bulb_id", "ip")


class NameSerializer(ModelSerializer):
    class Meta:
        model = YeelightBulb
        fields = ("name",)
