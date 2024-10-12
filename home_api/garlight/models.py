from django.db.models import CharField, Model, IntegerField


class YeelightBulb(Model):
    bulb_id = CharField(max_length=32, unique=True)
    ip = CharField(max_length=15, unique=True)
    name = CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}-{self.bulb_id}, ip:{self.ip}"


class Temperature(Model):
    name = CharField(max_length=16, unique=True)
    kelvins = IntegerField(max_length=4)
    brightness = IntegerField(max_length=3)

    def __str__(self):
        return f"Temperature: {self.kelvins}K - {self.brightness}%"

    def clean(self):
        if self.kelvins not in range(1700, 6501):
            raise ValueError("Temperature out of range!")
        if self.brightness not in range(0, 101):
            raise ValueError("Brightness out of range!")
        return super().clean()


class Color(Model):
    name = CharField(max_length=16, unique=True)
    r = IntegerField(max_length=3)
    g = IntegerField(max_length=3)
    b = IntegerField(max_length=3)
    brightness = IntegerField(max_length=3)

    def __str__(self):
        return f"RGB: {self.r}, {self.g}, {self.b} - {self.brightness}%"

    def clean(self):
        if self.r not in range(0, 256):
            raise ValueError("Red out of range!")
        if self.g not in range(0, 256):
            raise ValueError("Green out of range!")
        if self.b not in range(0, 256):
            raise ValueError("Blue out of range!")
        if self.brightness not in range(0, 101):
            raise ValueError("Brightness out of range!")
        return super().clean()
