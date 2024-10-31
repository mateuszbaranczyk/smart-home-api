from django.contrib import admin
from garlight.models import Color, Endpoint, Temperature, Timer, YeelightBulb, Brightness

admin.site.register(YeelightBulb)
admin.site.register(Color)
admin.site.register(Temperature)
admin.site.register(Timer)
admin.site.register(Brightness)
admin.site.register(Endpoint)
