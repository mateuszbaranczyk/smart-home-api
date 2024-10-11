from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse
from garlight.bulbs import discover_bulbs
from garlight.models import YeelightBulb
from garlight.serializers import BulbSerializer, NameSerializer
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed, NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


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


class PowerViewSet(ReadOnlyModelViewSet):
    queryset = YeelightBulb.objects.all()
    serializer_class = NameSerializer
    lookup_field = "name"

    def retrieve(request: Request, *args, **kwargs):
        return Response("ok")


class ColorViewSet(ReadOnlyModelViewSet):
    queryset = YeelightBulb.objects.all()
    serializer_class = NameSerializer
    lookup_field = "name"

    def retrieve(request: Request, *args, **kwargs):
        try:
            color = list(request.request.query_params.keys())[0]
        except IndexError:
            raise NotFound(detail="Color not found")
        return Response(f"{color}")


class TemperatureViewSet(ReadOnlyModelViewSet):
    queryset = YeelightBulb.objects.all()
    serializer_class = NameSerializer
    lookup_field = "name"

    def retrieve(request: Request, *args, **kwargs):
        try:
            temperature = list(request.request.query_params.keys())[0]
        except IndexError:
            raise NotFound(detail="Temperature not found")
        return Response(f"{temperature}")
