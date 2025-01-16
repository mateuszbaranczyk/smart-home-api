from authentication.views import Auth
from django.http import HttpResponse
from garlight.views.bulb_actions import YeelightViewSet
from rest_framework.viewsets import ModelViewSet

from aura.adapters import AdapterResponse, WeatherAdapter
from aura.models import Location
from aura.serializers import LocationSerializer


class LocationViewSet(ModelViewSet, Auth):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class WeatherView(YeelightViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = "name"

    def get_weather_data(self):
        location = self.get_object()
        adapter = WeatherAdapter(location)
        weather_data = adapter.get_weather()
        return weather_data


class CurrentWeatherView(WeatherView):
    def retrieve(self, request, *args, **kwargs):
        weather_data = self.get_weather_data()
        result = self.create_text(weather_data)
        return HttpResponse(result, content_type="text/plain")

    def create_text(self, weather_data: AdapterResponse) -> str:
        if weather_data.error:
            return f"Adapter error: {weather_data.error}"
        current = weather_data.data.current
        current_temp = current.get("temp_c", "")
        current_feel = current.get("feelslike_c", "")
        current_wind = current.get("wind_kph", "")
        current_air = current.get("air_quality", {}).get("gb-defra-index", "")
        cond = current.get("condition", {}).get("text", "")
        text = f"Temp: {current_temp} C\nFeel: {current_feel} C\nWind: {current_wind} km/h\nAir: {current_air}/10\n{cond}"
        return text


class ForecastWeatherView(WeatherView):
    def retrieve(self, request, *args, **kwargs):
        weather_data = self.get_weather_data()
        result = self.create_text(weather_data)
        return HttpResponse(result, content_type="text/plain")

    def create_text(self, weather_data: AdapterResponse) -> str:
        if weather_data.error:
            return f"Adapter error: {weather_data.error}"
        forecast = weather_data.data.forecast.get("forecastday", [])
        try:
            forecast_temp = forecast[0]["hour"][2]["temp_c"]
            forecast_feel = forecast[0]["hour"][2]["feelslike_c"]
            forecast_wind = forecast[0]["hour"][2]["wind_kph"]
            cond = forecast[0]["hour"][2]["condition"]["text"]
        except (KeyError, IndexError):
            return "API response error"
        text = f"Temp: {forecast_temp} C\nFeel: {forecast_feel} C\nWind: {forecast_wind} km/h\n{cond}"
        return text
