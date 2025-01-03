from django.db import models


class Location_(models.Model):
    name = models.CharField(max_length=50)
    api_key = models.CharField(max_length=50)
    lat = models.FloatField()
    lon = models.FloatField()
    air_quality = models.BooleanField()
