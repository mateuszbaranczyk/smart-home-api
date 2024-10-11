from django.db.models import Model, CharField


class YeelightBulb(Model):
    bulb_id = CharField(max_length=32)
    ip = CharField(max_length=15)
    name = CharField(max_length=64)
