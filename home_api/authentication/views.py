from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import LoginSerializer


class Auth(APIView):
    permission_classes = [IsAdminUser]


class GarminAuth(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class LoginView(APIView):
    def get(self, request):
        serializer = LoginSerializer()
        return render(request, "login_django.html", {"serializer": serializer})

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            remember_me = serializer.validated_data["remember_me"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                if remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(1209600)

                return redirect("/")
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect("/")
