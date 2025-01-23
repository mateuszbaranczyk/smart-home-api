
from unittest.mock import patch

from django.test import TestCase

from aura.adapters import WeatherAdapter
from aura.models import Location
from aura.tests.response import eg_forecast_response


class WeatherAdapterTest(TestCase):
    def setUp(self):
        self.model = Location(name="test", lat=20, lon=20)
        self.adapter = WeatherAdapter(self.model)

    @patch("aura.adapters.requests.get")
    def test_get_weather(self, m_requests):
        m_requests.return_value.status_code = 200
        m_requests.return_value.json.return_value = eg_forecast_response
        adapter_response = self.adapter.get_weather()
        assert adapter_response.status_code == 200
        assert adapter_response.data.location['name'] == "Piastow"
