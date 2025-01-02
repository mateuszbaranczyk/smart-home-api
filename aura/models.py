from django.db import models


class Location(models.Model):
    api_key = models.CharField(max_length=50)
    lat = models.FloatField()
    lon = models.FloatField()
    name = models.CharField(max_length=50)
    air_quality = models.BooleanField()
