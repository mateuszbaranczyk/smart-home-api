from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse
from garlight.bulbs import discover_bulbs
from garlight.models import Timer, YeelightBulb, Color, Temperature
from garlight.serializers import (
    BulbSerializer,
    NameSerializer,
    ColorSerializer,
    TemperatureSerializer,
    TimerSerializer,
)
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from garlight.mixins import YellightViewMixin
from garlight.bulbs import SmartBulb


class BulbViewSet(ModelViewSet):
    queryset = YeelightBulb.objects.all()
    serializer_class = BulbSerializer
    lookup_field = "name"

    def create(self, request, *args, **kwargs):
        msg = "Please use 'bulbs/discover/' endpoint for discover and create new device"
        raise MethodNotAllowed("POST", detail=msg)

    @action(detail=False, methods=["get"])
    def discover(self, request: Request):
        discovered = discover_bulbs()
        existing = YeelightBulb.objects.all().values_list("bulb_id", flat=True)
        bulbs = self._create_db_obj(discovered, existing)
        YeelightBulb.objects.bulk_create(bulbs)
        return HttpResponseRedirect(reverse("bulbs-list"))

    def _create_db_obj(
        self, discovered: dict, existing: QuerySet
    ) -> list[YeelightBulb]:
        bulbs = [
            YeelightBulb(
                bulb_id=device["capabilities"]["id"],
                ip=device["ip"],
                name=device["capabilities"]["id"],
            )
            for device in discovered
            if device["capabilities"]["id"] not in existing
        ]
        return bulbs


class BulbPowerViewSet(ReadOnlyModelViewSet):
    queryset = YeelightBulb.objects.all()
    serializer_class = NameSerializer
    lookup_field = "name"

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        bulb = SmartBulb(instance)
        result = bulb.on_off()
        return Response(result)


class ColorViewSet(ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class TemperatureViewSet(ModelViewSet):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer


class TimerViewSet(ModelViewSet):
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer


class BulbColorViewSet(ReadOnlyModelViewSet, YellightViewMixin):
    queryset = YeelightBulb.objects.all()
    serializer_class = NameSerializer
    lookup_field = "name"

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        color_name = self.get_query_key(request)
        color = Color.objects.all().filter(name=color_name).first()
        bulb = SmartBulb(instance)
        result = bulb.set_color(color)
        return Response(result)


class BulbTemperatureViewSet(ReadOnlyModelViewSet, YellightViewMixin):
    queryset = YeelightBulb.objects.all()
    serializer_class = NameSerializer
    lookup_field = "name"

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        temperature_name = self.get_query_key(request)
        temperature = (
            Temperature.objects.all().filter(name=temperature_name).first()
        )
        bulb = SmartBulb(instance)
        result = bulb.set_temperature(temperature)
        return Response(result)


class BulbTimerViewSet(ReadOnlyModelViewSet, YellightViewMixin):
    queryset = YeelightBulb.objects.all()
    serializer_class = NameSerializer
    lookup_field = "name"

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        time = self.get_query_key(request)
        minutes = Timer.objects.all().filter(minutes=time).first().minutes
        bulb = SmartBulb(instance)
        result = bulb.set_timier(minutes)
        return Response(result)
