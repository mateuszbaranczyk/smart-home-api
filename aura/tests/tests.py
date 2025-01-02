from unittest.mock import MagicMock

from django.test import TestCase

from aura.tests.response import eg_forecast_response


class WeatherAdapterTest(TestCase):
    def setUp(self):
        self.model = MagicMock()
        self.model.key = 'test_key'
        self.model.lat = 20.0
        self.model.lon = 20.0
        self.model.name = 'city_name'
        self.model.air = True 
        self.adapter = MagicMock()
        self.adapter.get_weather.return_value=eg_forecast_response

    def test_get_weather(self):
        adapter_response = self.adapter.get_weather(self.model)
        assert adapter_response.status_code == 200
        assert adapter_response.json() == eg_forecast_response