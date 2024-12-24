from .api_connection import ApiConnection
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import csv

from .passwords import USERNAME, PASSWORD

import logging
logging.basicConfig(level=logging.INFO) #DEBUG, INFO, WARNING, ERROR, CRITICAL

from enum import Enum

_LOGGER = logging.getLogger(__name__)

class TimePeriod(Enum):
    DAY = 1
    MONTH = 2
    YEAR = 3


def authenticate():
    # Authenticate with the API    
    api = ApiConnection(USERNAME, PASSWORD)
    if api == None:
        raise Exception("Authentication failed")
    
    return api
    

def log_time(type:TimePeriod, keys, systemDict):
    if type == TimePeriod.DAY:
        date = datetime.today().date()
    elif type == TimePeriod.MONTH:
        date = datetime.today().date().replace(day=1)
    elif type == TimePeriod.YEAR:
        date = datetime.today().date().replace(month=1, day=1)

    fileName = f"{systemDict['name']}_system_data_{type.name}.csv"
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


        for i in [0,1]:
            if type == TimePeriod.DAY:
                newDate = str(date - timedelta(days=i+1))
            elif type == TimePeriod.MONTH:
                newDate = str(date - relativedelta(months=i+1))
            elif type == TimePeriod.YEAR:
                newDate = str(date - relativedelta(years=i+1))
            usage = [newDate]

            for j in keys:
                if j != "Date":
                    usage.append(systemDict["energy"]["usage"][f"{type.name.lower()}{i+1}"][j])

            # _LOGGER.info(usage)

            _LOGGER.info(f"At {systemDict['name']} gas usage is {usage[keys.index('gas')]} for {newDate}")
            if newDate not in allDates:
                writer.writerow(usage)



if __name__ == "__main__":
    api: ApiConnection = authenticate()
    
    systems = api.get_systems()

    for system in systems:
        systemDict = system.__repr__()
        keys = [i if i != "$" else "Date" for i in systemDict["energy"]["usage"][f"day1"].keys()]
        _LOGGER.info(f"Keys are {keys}")

        log_time(TimePeriod.DAY, keys, systemDict)
        log_time(TimePeriod.MONTH, keys, systemDict)
        # log_time(TimePeriod.YEAR, keys, systemDict) #current year is logged through todays date which makes logging weird



        


