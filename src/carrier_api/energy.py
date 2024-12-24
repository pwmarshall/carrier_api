import logging

from dateutil.parser import isoparse
import datetime

from .util import safely_get_json_value

_LOGGER = logging.getLogger(__name__)


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
        self.raw_profile_json = self.system.api_connection.get_energy(
            system_serial=self.system.serial
        )
        _LOGGER.debug(f"raw_profile_json:{self.raw_profile_json}")
        self.usage = safely_get_json_value(self.raw_profile_json, "usage")
        self.cost = safely_get_json_value(self.raw_profile_json, "cost")

    def __repr__(self):
        return {
            "usage": self.usage,
            "cost": self.cost,
        }

    def __str__(self):
        return str(self.__repr__())
