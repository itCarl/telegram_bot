
# a Simple script that fetches, every 10 minutes, weather data from openweathermap.org


import os
import requests
import json
import sched, time
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('OWTOKEN')
s = sched.scheduler(time.time, time.sleep)
waitTime = 600 # 60*10= 600 seconds = 10 Minutes


def fetchWeatherData(sc):
    response = requests.get("http://api.openweathermap.org/data/2.5/weather", p)
    print("fetched Weather @ " + datetime.now().strftime("%H:%M:%S"))
    with open('SnakeTamer/weather-data.json', 'w') as outfile:
        json.dump(response.json(), outfile)
    s.enter(waitTime, 1, fetchWeatherData, (sc,))

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

    
p = {
    "id": "2945358",        # City ID, 2945358 = Brandenburg an der Havel
    "units": "metric",
    "APPID": TOKEN
}

fetchWeatherData(s)

s.enter(waitTime, 1, fetchWeatherData, (s,))
s.run()
