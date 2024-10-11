from rest_framework.serializers import ModelSerializer

from garlight.models import YeelightBulb


class BulbSerializer(ModelSerializer):
    class Meta:
        model = YeelightBulb
        fields = "__all__"
        read_only_fields = ("bulb_id", "ip")
