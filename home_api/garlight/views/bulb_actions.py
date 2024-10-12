from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse
from garlight.bulbs import SmartBulb, discover_bulbs
from garlight.models import Color, Temperature, Timer, YeelightBulb
from garlight.serializers import BulbSerializer, NameSerializer
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed, NotFound
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet


class BulbViewSet(ModelViewSet):
    queryset = YeelightBulb.objects.all()
    serializer_class = BulbSerializer
    lookup_field = "name"

    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        context["urls"] = self._get_action_urls()
        return context

    def _get_action_urls(self) -> dict:
        actions = {
            "sypialnia": self._generate_urls("sypialnia"),
            "salon": self._generate_urls("salon"),
        }
        return actions

    def _generate_urls(
        self,
        device,
    ) -> list:
        host = "localhost:8000"
        endpoints = ["timer", "temperature", "color"]
        color_presets = ["red", "purple"]
        temperature_presets = ["cold", "warm"]
        timer_presets = ["15", "30"]
        on_off = f"{host}/on-off/{device}/"
        urls = []
        urls.append(on_off)
        for endpoint in endpoints:
            if endpoint == "color":
                for color in color_presets:
                    url = f"{host}/{endpoint}/{device}?{color}"
                    urls.append(url)
            elif endpoint == "temperature":
                for temperature in temperature_presets:
                    url = f"{host}/{endpoint}/{device}?{temperature}"
                    urls.append(url)
            elif endpoint == "timer":
                for timer in timer_presets:
                    url = f"{host}/{endpoint}/{device}?{timer}"
                    urls.append(url)
        return urls

    def create(self, request: Request, *args, **kwargs):
        msg = "Please use 'bulbs/discover/' endpoint for discover and create new device"
        raise MethodNotAllowed("POST", detail=msg)

    @action(detail=False, methods=["get"])
    def discover(self, request: Request):
        discovered = discover_bulbs()
        existing = YeelightBulb.objects.all().values_list("bulb_id", flat=True)
        bulbs = self._create_db_obj(discovered, existing)
        YeelightBulb.objects.bulk_create(bulbs)
        return HttpResponseRedirect(reverse("bulb-list"))

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


class YellightViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = YeelightBulb.objects.all()
    serializer_class = NameSerializer
    lookup_field = "name"

    def get_query_key(self, request: Request) -> str:
        try:
            keys = list(request.query_params.keys())[0]
        except IndexError:
            raise NotFound(detail="Query keys not found")
        return keys


class BulbPowerViewSet(YellightViewSet):
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        bulb = SmartBulb(instance)
        result = bulb.on_off()
        return Response(result)


class BulbColorViewSet(YellightViewSet):
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        color_name = self.get_query_key(request)
        color = Color.objects.all().filter(name=color_name).first()
        bulb = SmartBulb(instance)
        result = bulb.set_color(color)
        return Response(result)


class BulbTemperatureViewSet(YellightViewSet):
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        temperature_name = self.get_query_key(request)
        temperature = Temperature.objects.all().filter(name=temperature_name).first()
        bulb = SmartBulb(instance)
        result = bulb.set_temperature(temperature)
        return Response(result)


class BulbTimerViewSet(YellightViewSet):
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        time = self.get_query_key(request)
        minutes = Timer.objects.all().filter(minutes=time).first().minutes
        bulb = SmartBulb(instance)
        result = bulb.set_timier(minutes)
        return Response(result)
