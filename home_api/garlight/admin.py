from django.contrib import admin
from garlight.models import Color, Temperature, YeelightBulb, Timer, Endpoint

admin.site.register(YeelightBulb)
admin.site.register(Color)
admin.site.register(Temperature)
admin.site.register(Timer)
admin.site.register(Endpoint)
