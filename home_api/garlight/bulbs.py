from yeelight import Bulb, CronType, SceneClass, discover_bulbs
from garlight.models import YeelightBulb, Color, Temperature


class BulbException(Exception):
    pass


class SmartBulb:
    def __init__(self, db_model: YeelightBulb) -> None:
        self.model = db_model
        self.bulb = Bulb(ip=self.model.ip)

    def __repr__(self) -> str:
        return f"{self.model.name} - {self.check_state()}"

    @property
    def state(self):
        return f"{self.model.name} - {self.check_state()}"

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
        """Temperature in range 1700-6500, brightness 0-100"""
        status = self.bulb.set_scene(
            SceneClass.CT, temperature.kelvins, temperature.brightness
        )
        return self._status_return(status)

    def _status_return(sefl, status: str) -> str:
        if status == "ok":
            return "Ok"
        return "Failed"


def discover_and_assign() -> None:
    devices = discover_bulbs()
    return devices
