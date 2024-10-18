from garlight.models import Brightness, Color, Endpoint, Temperature, Timer
from garlight.serializers import (
    BrightnessSerializer,
    ColorSerializer,
    EndpointSerializer,
    TemperatureSerializer,
    TimerSerializer,
)
from rest_framework.viewsets import ModelViewSet


class ColorViewSet(ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class TemperatureViewSet(ModelViewSet):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer


class TimerViewSet(ModelViewSet):
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer


class BrightnessViewSet(ModelViewSet):
    queryset = Brightness.objects.all()
    serializer_class = BrightnessSerializer


class EndpointViewSet(ModelViewSet):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
