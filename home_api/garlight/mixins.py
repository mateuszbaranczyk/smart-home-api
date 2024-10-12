from rest_framework.exceptions import NotFound
from rest_framework.request import Request

from garlight.models import YeelightBulb
from garlight.serializers import NameSerializer


class YellightViewMixin:
    queryset = YeelightBulb.objects.all()
    serializer_class = NameSerializer
    lookup_field = "name"

    def get_query_key(self, request: Request) -> str:
        try:
            keys = list(request.query_params.keys())[0]
        except IndexError:
            raise NotFound(detail="Query keys not found")
        return keys
