from .api_connection import ApiConnection
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import csv

from .passwords import USERNAME, PASSWORD
from .const import TimePeriod

import logging
logging.basicConfig(level=logging.INFO) #DEBUG, INFO, WARNING, ERROR, CRITICAL

_LOGGER = logging.getLogger(__name__)


if __name__ == "__main__":
    api = ApiConnection(USERNAME, PASSWORD)
    if api == None:
        raise Exception("Authentication failed")
    
    systems = api.get_systems()

    for system in systems:
        keys = system.energy.get_usage_types()

        _LOGGER.info(f"Keys are {keys}")

        system.energy.log_usage(TimePeriod.DAY, keys, f"{system.__repr__()['name']}_system_data_day.csv")
        system.energy.log_usage(TimePeriod.MONTH, keys, f"{system.__repr__()['name']}_system_data_month.csv")



        


