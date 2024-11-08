from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings

from rest_framework.views import APIView


class Auth(APIView):
    is_developer = settings.DEVELOPER
    permission_classes = [
        IsAuthenticated if is_developer == "False" else AllowAny
    ]
