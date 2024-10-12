from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse
from garlight.bulbs import discover_bulbs
from garlight.models import YeelightBulb, Color, Temperature
from garlight.serializers import (
    BulbSerializer,
    NameSerializer,
    ColorSerializer,
    TemperatureSerializer,
)
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed, NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from garlight.mixins import YellightViewMixin


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

    def retrieve(request: Request, *args, **kwargs):
        return Response("ok")


class ColorViewSet(ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class TemperatureViewSet(ModelViewSet):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer


class BulbColorViewSet(ReadOnlyModelViewSet, YellightViewMixin):
    queryset = YeelightBulb.objects.all()
    serializer_class = NameSerializer
    lookup_field = "name"

    def retrieve(self, request: Request, *args, **kwargs):
        color = self.get_query_key(request)
        color_data = Color.objects.all().filter(name=color).first()
        return Response(f"{color_data}")


class BulbTemperatureViewSet(ReadOnlyModelViewSet, YellightViewMixin):
    queryset = YeelightBulb.objects.all()
    serializer_class = NameSerializer
    lookup_field = "name"

    def retrieve(self, request: Request, *args, **kwargs):
        temperature = self.get_query_key(request)
        temperature_data = (
            Temperature.objects.all().filter(name=temperature).first()
        )
        return Response(f"{temperature_data}")
