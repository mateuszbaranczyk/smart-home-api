from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.request import Request

from garlight.bulbs import discover_bulbs
from garlight.models import YeelightBulb
from garlight.serializers import BulbSerializer


class BulbViewSet(viewsets.ModelViewSet):
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
        return HttpResponseRedirect(reverse("yeelightbulb-list"))

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
