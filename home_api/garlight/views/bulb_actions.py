from typing import List
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from garlight.bulbs import BulbInfo, SmartBulb
from garlight.models import Color, Endpoint, Temperature, Timer, YeelightBulb
from garlight.serializers import BulbSerializer, NameSerializer
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed, NotFound
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from yeelight import discover_bulbs


class BulbViewSet(ModelViewSet):
    queryset = YeelightBulb.objects.all()
    serializer_class = BulbSerializer
    lookup_field = "name"

    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        context["urls"] = Endpoint.objects.all()
        return context

    def create(self, request: Request, *args, **kwargs):
        msg = "Please use 'bulbs/discover/' endpoint for discover and create new device"
        raise MethodNotAllowed("POST", detail=msg)

    @action(detail=False, methods=["get"])
    def discover(self, request: Request):
        discovered = self.fetch_discovered_bulbs()
        existing = YeelightBulb.objects.all().values_list("bulb_id", flat=True)
        bulbs = self.create_db_obj(discovered, existing)
        YeelightBulb.objects.bulk_create(bulbs)
        return HttpResponseRedirect(reverse("bulb-list"))

    def fetch_discovered_bulbs(self) -> list[BulbInfo]:
        discovered = discover_bulbs()
        if discovered == []:
            raise NotFound(detail="Devices not found")
        return [[BulbInfo(**device) for device in discovered]]

    def create_db_obj(
        self, discovered: list[BulbInfo], existing: QuerySet
    ) -> list[YeelightBulb]:
        bulbs = [
            YeelightBulb(
                bulb_id=device.properties.id,
                ip=device.ip,
                name=device.properties.id,
            )
            for device in discovered
            if device.properties.id not in existing
        ]
        return bulbs


class YeelightViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = YeelightBulb.objects.all()
    serializer_class = NameSerializer
    lookup_field = "name"

    def get_query_key(self, request: Request) -> str:
        try:
            keys = list(request.query_params.keys())[0]
        except IndexError:
            raise NotFound(detail="Query keys not found")
        return keys


class GarminEndpointsViewSet(ListModelMixin, GenericViewSet):
    def list(self, request: Request, *args, **kwargs):
        endpoints = [endpoint.path for endpoint in Endpoint.objects.all()]
        return HttpResponse(str(endpoints), content_type="text/plain")


class BulbPowerViewSet(YeelightViewSet):
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        bulb = SmartBulb(instance)
        result = bulb.on_off()
        return HttpResponse(result, content_type="text/plain")


class BulbColorViewSet(YeelightViewSet):
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        color_name = self.get_query_key(request)
        color = Color.objects.filter(name=color_name).first()
        bulb = SmartBulb(instance)
        result = bulb.set_color(color)
        return HttpResponse(result, content_type="text/plain")


class BulbTemperatureViewSet(YeelightViewSet):
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        temperature_name = self.get_query_key(request)
        temperature = Temperature.objects.filter(name=temperature_name).first()
        bulb = SmartBulb(instance)
        result = bulb.set_temperature(temperature)
        return HttpResponse(result, content_type="text/plain")


class BulbTimerViewSet(YeelightViewSet):
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        time = self.get_query_key(request)
        minutes = Timer.objects.filter(minutes=time).first().minutes
        bulb = SmartBulb(instance)
        result = bulb.set_timier(minutes)
        return HttpResponse(result, content_type="text/plain")

class BrightnessViewSet(YeelightViewSet):
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        brightness = self.get_query_key(request)
        bulb = SmartBulb(instance)
        result = bulb.set_brightness(brightness)
        return HttpResponse(result, content_type="text/plain")