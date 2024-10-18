from django.db.models import CASCADE, CharField, ForeignKey, IntegerField, Model


class YeelightBulb(Model):
    bulb_id = CharField(max_length=32, unique=True)
    ip = CharField(max_length=15, unique=True)
    name = CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name} - {self.bulb_id}, ip:{self.ip}"


class Temperature(Model):
    name = CharField(max_length=16, unique=True)
    kelvins = IntegerField()
    brightness = IntegerField()

    def __str__(self):
        return f"Temperature: {self.kelvins}K - {self.brightness}%"


class Color(Model):
    name = CharField(max_length=16, unique=True)
    r = IntegerField()
    g = IntegerField()
    b = IntegerField()
    brightness = IntegerField()

    def __str__(self):
        return f"RGB: {self.r}, {self.g}, {self.b} - {self.brightness}%"


class Timer(Model):
    minutes = IntegerField(unique=True)

    def __str__(self):
        return f"Timer {self.minutes}"


def presets() -> dict[str, str]:
    color = [
        (color_preset, "Color - " + color_preset)
        for color_preset in Color.objects.all().values_list("name", flat=True)
    ]
    temperature = [
        (color_preset, "Temperature - " + color_preset)
        for color_preset in Temperature.objects.all().values_list("name", flat=True)
    ]
    timer = [
        (str(color_preset), "Timer - " + str(color_preset))
        for color_preset in Timer.objects.all().values_list("minutes", flat=True)
    ]
    power = [("power", "Power")]
    presets = power + color + temperature + timer

    return {preset[0]: preset[1] for preset in presets}


class Endpoint(Model):
    ACTIONS = [
        ("on-off", "Power"),
        ("color", "Color"),
        ("timer", "Timer"),
        ("temperature", "Temperature"),
    ]

    name = CharField(max_length=32, unique=True)
    action = CharField(max_length=16, choices=ACTIONS)
    device = ForeignKey(YeelightBulb, on_delete=CASCADE)
    preset = CharField(max_length=16, choices=presets)

    @property
    def path(self):
        return f"/{self.action}/{self.device.name}/?{self.preset}"

    def __str__(self):
        return f"/{self.action}/{self.device.name}/?{self.preset}"
