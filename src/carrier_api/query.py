from .api_connection import ApiConnection
import json
from datetime import datetime, timedelta
import csv

from .passwords import USERNAME, PASSWORD

import logging
logging.basicConfig(level=logging.DEBUG) #DEBUG, INFO, WARNING, ERROR, CRITICAL


_LOGGER = logging.getLogger(__name__)

def authenticate():
    # Authenticate with the API    
    api = ApiConnection(USERNAME, PASSWORD)
    if api == None:
        raise Exception("Authentication failed")
    
    return api
    

if __name__ == "__main__":
    api: ApiConnection = authenticate()
    
    systems = api.get_systems()

    for system in systems:
        systemDict = system.__repr__()
        print(systemDict["name"])
        if systemDict["name"] == "Rabbit":
            date = datetime.today().date()
            
            try:
                with open("system_data.csv", mode='r') as file:
                    reader = csv.DictReader(file)
                    allDates = [row["Date"] for row in reader]
            except FileNotFoundError:
                allDates = []


            with open("system_data.csv", mode='a', newline="\n") as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(["Date", "Usage"])
   

                for i in [0,1]:
                    usage = int(systemDict["energy"]["usage"]["period"][i]["gas"])
                    newDate = str(date - timedelta(days=i+1))
                    _LOGGER.info(f"Date: {newDate}, Usage: {usage}")
                    if newDate not in allDates:
                        writer.writerow([newDate, usage])


