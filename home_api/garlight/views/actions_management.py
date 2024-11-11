from authentication.views import Auth
from garlight.models import Brightness, Color, Endpoint, Temperature, Timer
from garlight.serializers import (
    BrightnessSerializer,
    ColorSerializer,
    EndpointSerializer,
    TemperatureSerializer,
    TimerSerializer,
)
from rest_framework.viewsets import ModelViewSet


class ColorViewSet(ModelViewSet, Auth):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class TemperatureViewSet(ModelViewSet, Auth):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer


class TimerViewSet(ModelViewSet, Auth):
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer


class BrightnessViewSet(ModelViewSet, Auth):
    queryset = Brightness.objects.all()
    serializer_class = BrightnessSerializer


class EndpointViewSet(ModelViewSet, Auth):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
