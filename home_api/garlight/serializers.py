from rest_framework.serializers import ModelSerializer
from garlight.models import YeelightBulb


class BulbSerializer(ModelSerializer):
    class Meta:
        model = YeelightBulb
        fields = '__all__'