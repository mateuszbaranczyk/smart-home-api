from django.contrib import admin

from garlight.models import (
    Brightness,
    Color,
    Endpoint,
    Temperature,
    Timer,
    YeelightBulb,
)

admin.site.register(YeelightBulb)
admin.site.register(Color)
admin.site.register(Temperature)
admin.site.register(Timer)
admin.site.register(Brightness)
admin.site.register(Endpoint)
