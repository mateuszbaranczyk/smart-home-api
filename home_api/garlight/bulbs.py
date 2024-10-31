from dataclasses import dataclass
from garlight.models import Color, Temperature, YeelightBulb
from yeelight import Bulb, CronType, SceneClass


class BulbException(Exception):
    pass


class SmartBulb:
    def __init__(self, db_model: YeelightBulb) -> None:
        self.db_model = db_model
        self.bulb = Bulb(ip=self.db_model.ip)

    def __repr__(self) -> str:
        return f"{self.db_model.name} - {self.check_state()}"

    @property
    def state(self):
        return f"{self.db_model.name} - {self.check_state()}"

    def on_off(self) -> str:
        power = self.check_state()
        try:
            msg = self.change_state(power)
            return f"{msg}"
        except Exception as err:
            raise BulbException(err)

    def change_state(self, power_status: str) -> str:
        match power_status:
            case "offline":
                return "Offline"
            case "on":
                self.bulb.turn_off()
                return "Power off"
            case "off":
                self.bulb.turn_on()
                return "Power on"

    def check_state(self) -> str:
        """'on' | 'off' | 'offline'"""
        data = self.bulb.get_capabilities()
        state = data["power"] if data else "offline"
        return state

    def set_timier(self, minutes: int = 15):
        status = self.bulb.cron_add(CronType.off, minutes)
        if status == "ok":
            return f"Timer to {minutes} min."
        return "Failed"

    def set_color(self, color: Color) -> str:
        status = self.bulb.set_scene(
            SceneClass.COLOR, color.r, color.g, color.b, color.brightness
        )
        return self._status_return(status)

    def set_temperature(self, temperature: Temperature) -> str:
        """Temperature in range 1700-6500, brightness 1-100"""
        status = self.bulb.set_scene(
            SceneClass.CT, temperature.kelvins, temperature.brightness
        )
        return self._status_return(status)

    def _status_return(sefl, status: str) -> str:
        if status == "ok":
            return "Ok"
        return "Failed"

    def set_brightness(self, brightness: int) -> str:
        """Temperature in range 1-100"""
        status = self.bulb.set_brightness(brightness)
        return self._status_return(status)

@dataclass(frozen=True)
class Properties:
    id: str
    model: str
    fw_ver: str
    support: str
    power: str
    bright: str
    color_mode: str
    ct: str
    rgb: str
    hue: str
    sat: str
    name: str


@dataclass(frozen=True)
class BulbInfo:
    ip: str
    port: int
    capabilities: dict

    @property
    def properties(self) -> Properties:
        return Properties(**self.capabilities)
