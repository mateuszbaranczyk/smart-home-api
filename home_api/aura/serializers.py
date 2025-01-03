from rest_framework.serializers import ModelSerializer

from aura.models import Location_


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location_
        fields = "__all__"
