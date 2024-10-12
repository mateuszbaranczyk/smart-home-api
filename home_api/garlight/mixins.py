from rest_framework.exceptions import NotFound
from rest_framework.request import Request


class YellightViewMixin:
    def get_query_key(request: Request) -> str:
        try:
            keys = list(request.request.query_params.keys())[0]
        except IndexError:
            raise NotFound(detail="Query keys not found")
        return keys
