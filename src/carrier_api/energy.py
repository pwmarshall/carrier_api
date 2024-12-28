import csv
import logging

from .const import TimePeriod
from .util import safely_get_json_value
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


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
    
    def get_usage_types(self) -> list:
        return [i for i in self.usage.__repr__()["day1"].keys() if i != "$"]
    
    def log_usage(self, type:TimePeriod, keys, fileName):
        if type == TimePeriod.DAY:
            date = datetime.today().date()
        elif type == TimePeriod.MONTH:
            date = datetime.today().date().replace(day=1)
        elif type == TimePeriod.YEAR:
            _LOGGER.info("Year Logging Not Fully Implemented Yet")
            date = datetime.today().date().replace(month=1, day=1)
        else:
            raise ValueError(f"{type} is not a valid Logging Time Period")
        
        if keys[0] != "Date":
            keys.insert(0,"Date")

        if fileName[-4:] != ".csv":
            raise ValueError(f"{fileName} is not a csv file")

        try:
            with open(fileName, mode='r') as file:
                reader = csv.DictReader(file)
                allDates = [row["Date"] for row in reader]
        except FileNotFoundError:
            allDates = []


        with open(fileName, mode='a', newline="\n") as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(keys)

            for i in [0,1]: #api only returns 2 days/months
                if type == TimePeriod.DAY:
                    newDate = str(date - timedelta(days=i+1))
                elif type == TimePeriod.MONTH:
                    newDate = str(date - relativedelta(months=i+1))
                elif type == TimePeriod.YEAR:
                    newDate = str(date - relativedelta(years=i+1))

                usage = [newDate]

                for j in keys:
                    if j != "Date":
                        try:
                            usage.append(self.__repr__()["usage"][f"{type.name.lower()}{i+1}"][j])
                        except KeyError:
                            raise KeyError(f"{j} is not a valid usage type")

                if newDate not in allDates:
                    writer.writerow(usage)
