from yeelight import Bulb, CronType, SceneClass, discover_bulbs


class BulbException(Exception):
    pass


class HomeBulb:
    def __init__(self, name: str) -> None:
        self.model = self.get_from_db(name)
        self.bulb = Bulb(ip=self.model.ip)

    def __repr__(self) -> str:
        return f"{self.model.name} - {self.check_state()}"

    @property
    def state(self):
        return f"{self.model.name} - {self.check_state()}"

    def get_from_db(self, name: str):
        model = db.session.execute(
            db.select(BulbModel).filter_by(name=name)
        ).scalar_one()
        return model

    def on_off(self) -> str:
        power = self.check_state()
        try:
            msg = self.change_state(power)
            return f"{msg}"
        except Exception as err:
            gunicorn_logger.error(f"Bulb - {self.bulb_name} - {err}")
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

    def set_color(self, red: int, green: int, blue: int, brightness: int) -> str:
        """Colors in range 0-255, brightness 0-100"""
        self._validate_colors(red, green, blue, brightness)
        status = self.bulb.set_scene(SceneClass.COLOR, red, green, blue, brightness)
        return self._status_return(status)

    def set_temperature(self, temperature: int, brightness: int) -> str:
        """Temperature in range 1700-6500, brightness 0-100"""
        self._validate_temperature(temperature, brightness)
        status = self.bulb.set_scene(SceneClass.CT, temperature, brightness)
        return self._status_return(status)

    def _status_return(sefl, status: str) -> str:
        if status == "ok":
            return str.capitalize(status)
        return "Failed"

    def _validate_temperature(sefl, temperature: int, brightness: int) -> None:
        if temperature not in range(1700, 6501):
            raise ValueError("Temperature out of range!")

        if brightness not in range(0, 101):
            raise ValueError("Brightness out of range!")

    def _validate_colors(
        self, red: int, green: int, blue: int, brightness: int
    ) -> None:
        if red not in range(0, 256):
            raise ValueError("Red out of range!")
        if green not in range(0, 256):
            raise ValueError("Green out of range!")
        if blue not in range(0, 256):
            raise ValueError("Blue out of range!")
        if brightness not in range(0, 101):
            raise ValueError("Brightness out of range!")


def discover_and_assign() -> None:
    devices = discover_bulbs()
    return devices


def bulb_exists(bulb_id: str) -> bool:
    exists = db.session.query(literal(True)).filter(BulbModel.id == bulb_id).first()
    if exists:
        return exists[0]
    return False
