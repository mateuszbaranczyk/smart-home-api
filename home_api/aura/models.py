from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=50)
    lat = models.FloatField()
    lon = models.FloatField()
