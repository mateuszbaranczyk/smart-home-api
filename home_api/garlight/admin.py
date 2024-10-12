from django.contrib import admin

from garlight.models import Color, Temperature, YeelightBulb

admin.site.register(YeelightBulb)
admin.site.register(Color)
admin.site.register(Temperature)
