from aura.adapters import AdapterResponse, WeatherAdapter, WeatherForecast
from aura.models import Location_
from aura.tests.response import eg_forecast_response
from django.test import TestCase


class WeatherAdapterTest(TestCase):
    def setUp(self):
        self.model = Location_(
            name="test", lat=20, lon=20, api_key="test", air_quality=False
        )
        self.adapter = WeatherAdapter(self.model)

    # @mock request
    def test_get_weather(self):
        expected_response_data = WeatherForecast(**eg_forecast_response)
        self.adapter.get_weather.return_value = AdapterResponse(
            status_code=200, data=expected_response_data
        )
        adapter_response = self.adapter.get_weather(self.model)
        assert adapter_response.status_code == 200
        assert adapter_response.data.location.name == "Piastow"
