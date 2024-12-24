import logging

from .util import safely_get_json_value

_LOGGER = logging.getLogger(__name__)

class Energy_Usage:
    def __init__(self, raw_usage_json):
        self.times = []
        periods = safely_get_json_value(raw_usage_json, "period")
        for i in range(6):
            self.times.append(periods[i])

    def __repr__(self):
        return {
            "day1": self.times[0],
            "day2": self.times[1],
            "month1": self.times[2],
            "month2": self.times[3],
            "year1": self.times[4],
            "year2": self.times[5],
        }

    def __str__(self):
        return str(self.__repr__())

class Energy_Cost:
    def __init__(self, raw_cost_json):
        self.times = []
        periods = safely_get_json_value(raw_cost_json, "period")
        for i in range(6):
            self.times.append(periods[i])

    def __repr__(self):
        return {
            "day1": self.times[0],
            "day2": self.times[1],
            "month1": self.times[2],
            "month2": self.times[3],
            "year1": self.times[4],
            "year2": self.times[5],
        }

    def __str__(self):
        return str(self.__repr__())

class Energy:
    usage: str = None
    cost: str = None

    def __init__(
        self,
        system,
    ):
        self.system = system
        self.refresh()

    def refresh(self):
        self.raw_energy_json = self.system.api_connection.get_energy(
            system_serial=self.system.serial
        )
        _LOGGER.debug(f"raw_profile_json:{self.raw_energy_json}")
        self.usage = Energy_Usage(safely_get_json_value(self.raw_energy_json, "usage"))
        self.cost = Energy_Cost(safely_get_json_value(self.raw_energy_json, "cost"))

    def __repr__(self):
        return {
            "usage": self.usage.__repr__(),
            "cost": self.cost.__repr__(),
        }

    def __str__(self):
        return str(self.__repr__())
