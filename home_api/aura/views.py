from authentication.views import Auth
from django.http import HttpResponse
from garlight.views.bulb_actions import YeelightViewSet
from rest_framework.viewsets import ModelViewSet

from aura.adapters import AdapterResponse, WeatherAdapter
from aura.models import Location_
from aura.serializers import LocationSerializer


class LocationViewSet(ModelViewSet, Auth):
    queryset = Location_.objects.all()
    serializer_class = LocationSerializer


class CurrentWeatherView(YeelightViewSet):
    queryset = Location_.objects.all()
    serializer_class = LocationSerializer
    lookup_field = "name"

    def retrieve(self, request, *args, **kwargs):
        location = self.get_object()
        adapter = WeatherAdapter(location)
        weather_data = adapter.get_weather()
        weather_text = self.create_text(weather_data)
        return HttpResponse(weather_text, content_type="text/plain")

    def create_text(self, weather_data: AdapterResponse) -> str:
        if weather_data.error:
            return weather_data.error
        if weather_data.data:
            current = weather_data.data.current
            forecast = weather_data.data.forecast
            current_temp = current.temp_c
            current_feel = current.feelslike_c
            current_wind = current.wind_kph
            current_air = current.air_quality.gb_defra_index
            forecast_temp = forecast.forecastday[0].hour[2].temp_c
            forecast_feel = forecast.forecastday[0].hour[2].feelslike_c
            forecast_wind = forecast.forecastday[0].hour[2].wind_kph
            forecast_air = (
                forecast.forecastday[0].hour[2].air_quality.gb_defra_index
            )
        return f""
