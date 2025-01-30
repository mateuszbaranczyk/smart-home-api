from aura.models import Location
from authentication.views import Auth, GarminAuth
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed, NotFound
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from yeelight import discover_bulbs

from garlight.bulbs import BulbInfo, SmartBulb
from garlight.models import (
    Brightness,
    Color,
    Endpoint,
    Temperature,
    Timer,
    YeelightBulb,
)
from garlight.serializers import BulbSerializer, NameSerializer


class BulbViewSet(ModelViewSet, Auth):
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
        bulbs = self.create_db_obj(discovered, existing)  # type: ignore
        YeelightBulb.objects.bulk_create(bulbs)
        return HttpResponseRedirect(reverse("bulb-list"))

    def fetch_discovered_bulbs(self) -> list[BulbInfo]:
        discovered = discover_bulbs()
        if discovered == []:
            raise NotFound(detail="Devices not found")
        return [BulbInfo(**device) for device in discovered]

    def create_db_obj(
        self, discovered: list[BulbInfo], existing: QuerySet[YeelightBulb]
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


class YeelightViewSet(RetrieveModelMixin, GenericViewSet, GarminAuth):
    queryset = YeelightBulb.objects.all()
    serializer_class = NameSerializer
    lookup_field = "name"

    def get_query_key(self, request: Request) -> str:
        try:
            keys = list(request.query_params.keys())[0]
        except IndexError:
            raise NotFound(detail="Query keys not found")
        return keys


class GarminEndpointsViewSet(ListModelMixin, GenericViewSet, GarminAuth):
    """Return a list of all endpoints for the Garmin device."""

    def list(self, request: Request, *args, **kwargs):
        all = "- all,Yeelight\n"
        device_names = Endpoint.objects.values_list(
            "device__name", flat=True
        ).distinct()
        by_device = [
            self.get_device_actions(device_name)
            for device_name in device_names
        ]
        weather = self.get_weather_endpoints()
        return HttpResponse(
            all + "".join(by_device) + weather, content_type="text/plain"
        )

    def get_weather_endpoints(self):
        endpoints = ""
        locations = Location.objects.values_list("name", flat=True).distinct()
        for location in locations:
            location_definition = (
                f"-- {location},{location.capitalize()} (Weather)\n"
            )
            current_endpoint = f"--- current,Current,/current/{location}\n"
            forecast_endpoint = f"--- forecast,Forecast,/forecast/{location}\n"
            endpoints += (
                location_definition + current_endpoint + forecast_endpoint
            )
        return endpoints

    def get_device_actions(self, device_name: str) -> str:
        endpoints_for_device = Endpoint.objects.filter(
            device__name=device_name
        )
        actions = endpoints_for_device.values_list(
            "action", flat=True
        ).distinct()
        actions_presets = [
            self.get_action_presets(
                action_name=action, device_name=device_name
            )
            for action in actions
        ]
        device_definitions = f"-- {device_name},{device_name.capitalize()}\n"
        return device_definitions + "".join(actions_presets)

    def get_action_presets(self, action_name: str, device_name: str) -> str:
        presets_for_action = Endpoint.objects.filter(
            action=action_name, device__name=device_name
        )
        action_definition = f"--- {action_name},{action_name.capitalize()}\n"
        presets = [
            f"---- {preset.name},{preset.name.capitalize()},{preset.path}\n"
            for preset in presets_for_action
        ]
        return action_definition + "".join(presets)


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
        result = bulb.set_timer(minutes)
        return HttpResponse(result, content_type="text/plain")


class BulbBrightnessViewSet(YeelightViewSet):
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        preset = self.get_query_key(request)
        brightness = Brightness.objects.filter(name=preset).first().brightness
        bulb = SmartBulb(instance)
        result = bulb.set_brightness(brightness)
        return HttpResponse(result, content_type="text/plain")
