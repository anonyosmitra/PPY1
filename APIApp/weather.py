from models.models import User,Coordinates,CurrentWeatherLoc,HourlyWeather,Weather
from dbHandler2 import Connect
import requests as HTTPRequests
from typing import List, Any
import timezone as tz
from datetime import datetime as dt
import json
codes={0: 'Clear Sky', 1: 'Mainly Clear', 2: 'Partly Cloudy', 3: 'Overcast', 45: 'Fog',
       48: 'Depositing Rime Fog', 51: 'Light Drizzle', 53: 'Moderate Drizzle', 55: 'Dense Drizzle',
       56: 'Light Freezing Drizzle', 57: 'Dense Freezing Drizzle', 61: 'Slight Rain', 63: 'Moderate Rain', 65: 'Heavy Rain',
       66: 'Light Freezing Rain', 67: 'Heavy Freezing Rain', 71: 'Slight Snow Fall', 73: 'Moderate Snow Fall', 75: 'Heavy Snow Fall',
       77: 'Snow Grains', 80: 'Slight Rain Showers', 81: 'Moderate Rain Showers', 82: 'Violent Rain Showers', 85: 'Slight Snow Showers',
       86: 'Heavy Snow Showers', 95: 'Thunderstorm', 96: 'Thunderstorm With Slight Hail', 99: 'Heavy Hail'}
api="https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}"
currentWeather="&current_weather=true"
hourly="&hourly=temperature_2m,weathercode"
imperial="&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch"

def getWeather(loc,user:User,con:Connect)->Weather:
       url = api + currentWeather
       if user.imperial:
              url += imperial
       weather = json.loads(HTTPRequests.get(url.format(loc["lat"], loc["lon"])).text)["current_weather"]
       return Weather(temp=weather["temperature"], weather=codes[weather["weathercode"]])
def getCurrentWeather(user:User,con:Connect)->List[CurrentWeatherLoc]:
       url=api+currentWeather
       resp=[]
       if user.imperial:
              url+=imperial
       for i in user.coordinates:
              weather=json.loads(HTTPRequests.get(url.format(i.lat,i.lon)).text)["current_weather"]
              resp.append(CurrentWeatherLoc(id=i.id,name=i.name,temp=weather["temperature"],weather=codes[weather["weathercode"]]))
       return resp
def getHourlyWeather(user:User,loc:Coordinates,con:Connect,zone=str)->List[HourlyWeather]:
       url=api+hourly
       resp=[]
       if user.imperial:
              url+=imperial
       weather=json.loads(HTTPRequests.get(url.format(loc.lat,loc.lon)).text)
       weather=weather["hourly"]
       for i in range(len(weather["time"])):
              h=HourlyWeather(
                     time=tz.convertTo(dt.strptime(weather["time"][i],"%Y-%m-%dT%H:%M"),zone,SysTZ="UTC",fmt="%H:%M"),
                     temp=weather["temperature_2m"][i],
                     weather=codes[weather["weathercode"][i]]
              )
              resp.append(h)
       return resp
