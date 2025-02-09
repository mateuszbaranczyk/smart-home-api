from dataclasses import dataclass
from typing import List, Optional, TypedDict

import requests
from django.conf import settings

from aura.models import Location


class AirQuality(TypedDict):
    co: float
    no2: float
    o3: float
    so2: float
    pm2_5: float
    pm10: float
    us_epa_index: int
    gb_defra_index: int


class Condition(TypedDict):
    text: str
    icon: str
    code: int


class Astro(TypedDict):
    sunrise: str
    sunset: str
    moonrise: str
    moonset: str
    moon_phase: str
    moon_illumination: int
    is_moon_up: int
    is_sun_up: int


class Hour(TypedDict):
    time_epoch: int
    time: str
    temp_c: float
    temp_f: float
    is_day: int
    condition: Condition
    wind_mph: float
    wind_kph: float
    wind_degree: int
    wind_dir: str
    pressure_mb: float
    pressure_in: float
    precip_mm: float
    precip_in: float
    snow_cm: float
    humidity: int
    cloud: int
    feelslike_c: float
    feelslike_f: float
    windchill_c: float
    windchill_f: float
    heatindex_c: float
    heatindex_f: float
    dewpoint_c: float
    dewpoint_f: float
    will_it_rain: int
    chance_of_rain: int
    will_it_snow: int
    chance_of_snow: int
    vis_km: float
    vis_miles: float
    gust_mph: float
    gust_kph: float
    uv: int
    air_quality: AirQuality


class Day(TypedDict):
    maxtemp_c: float
    maxtemp_f: float
    mintemp_c: float
    mintemp_f: float
    avgtemp_c: float
    avgtemp_f: float
    maxwind_mph: float
    maxwind_kph: float
    totalprecip_mm: float
    totalprecip_in: float
    totalsnow_cm: float
    avgvis_km: float
    avgvis_miles: float
    avghumidity: int
    daily_will_it_rain: int
    daily_chance_of_rain: int
    daily_will_it_snow: int
    daily_chance_of_snow: int
    condition: Condition
    uv: float
    air_quality: AirQuality


class ForecastDay(TypedDict):
    date: str
    date_epoch: int
    day: Day
    astro: Astro
    hour: List[Hour]


class Location_(TypedDict):
    name: str
    region: str
    country: str
    lat: float
    lon: float
    tz_id: str
    localtime_epoch: int
    localtime: str


class Current(TypedDict):
    last_updated_epoch: int
    last_updated: str
    temp_c: float
    temp_f: float
    is_day: int
    condition: Condition
    wind_mph: float
    wind_kph: float
    wind_degree: int
    wind_dir: str
    pressure_mb: float
    pressure_in: float
    precip_mm: float
    precip_in: float
    humidity: int
    cloud: int
    feelslike_c: float
    feelslike_f: float
    windchill_c: float
    windchill_f: float
    heatindex_c: float
    heatindex_f: float
    dewpoint_c: float
    dewpoint_f: float
    vis_km: float
    vis_miles: float
    uv: float
    gust_mph: float
    gust_kph: float
    air_quality: AirQuality


class Forecast(TypedDict):
    forecastday: List[ForecastDay]


@dataclass(frozen=True)
class WeatherForecast:
    location: Location_
    current: Current
    forecast: Forecast


@dataclass(frozen=True)
class AdapterResponse:
    status_code: int
    data: Optional[WeatherForecast] = None
    error: Optional[str] = None


class WeatherAdapter:
    """weatherapi.com"""

    def __init__(self, location: Location) -> None:
        api_key = settings.WEATHER_API_KEY
        url = "https://api.weatherapi.com/v1/forecast.json?"
        params = f"key={api_key}&q={location.lat},{location.lon}&days=1&aqi=yes&alerts=no"
        self.url = url + params

    def get_weather(self) -> AdapterResponse:
        response = requests.get(self.url)
        if response.status_code != 200:
            return AdapterResponse(
                status_code=response.status_code, error=response.json()
            )
        data = WeatherForecast(**response.json())
        return AdapterResponse(status_code=response.status_code, data=data)
