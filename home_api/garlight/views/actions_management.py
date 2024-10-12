from garlight.models import Color, Temperature, Timer
from garlight.serializers import ColorSerializer, TemperatureSerializer, TimerSerializer
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
