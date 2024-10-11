from django.db.models import Model, CharField


class YeelightBulb(Model):
    bulb_id = CharField(max_length=32, unique=True)
    ip = CharField(max_length=15, unique=True)
    name = CharField(max_length=64, unique=True)
