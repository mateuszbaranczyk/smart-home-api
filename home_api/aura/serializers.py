from rest_framework.serializers import ModelSerializer

from aura.models import Location


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
