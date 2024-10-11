from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.generics import GenericAPIView
from garlight.models import YeelightBulb
from garlight.serializers import BulbSerializer
from garlight.bulbs import discover_bulbs
from django.http import JsonResponse
from rest_framework.views import APIView


class BulbView(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericAPIView,
):
    queryset = YeelightBulb.objects.all()
    serializer_class = BulbSerializer

    def get(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class DeiscoverView(APIView):
    def get(self, request, *args, **kwargs):
        devices = discover_bulbs()
        return JsonResponse({"devices": devices})
