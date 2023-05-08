import pyowm
import os
import json

def get_weather(location):

    __location__ = os.path.dirname(os.path.abspath(__file__))

    with open (__location__ + "/ressource/config.json", "r") as f:
        config = json.load(f)
        api_key = config['App']['WEATHER_API']
        f.close()
    
    owm = pyowm.OWM(api_key)
    weather_mgr = owm.weather_manager()
    forecast = weather_mgr.forecast_at_place(location, interval='3h')

    forecast_interval = 4
    weatherList = forecast.forecast.weathers[0:forecast_interval]
    temp = 0
    feels = 0
    min = float('inf')
    max = float('-inf')
    description = {}

    for f in weatherList:
        temp = temp + ((f.temp['temp']- 273.15) * 1/forecast_interval)
        feels = feels + ((f.temp['feels_like']- 273.15) * 1/forecast_interval)
        if (f.temp['temp_min'] - 273.15) < min:
            min = (f.temp['temp_min'] - 273.15)
        if (f.temp['temp_max'] - 273.15) > min:
            max = (f.temp['temp_max'] - 273.15)
        if f.detailed_status in description:
            description[f.detailed_status] = description[f.detailed_status] + 1
        else:
            description[f.detailed_status] = 1
    try:
        description = max(description, key=description.get)
    except:
        description = "Wechselhaft"
    temp = round(temp,1)
    feels = round(feels,1)
    min = round(min, 1)
    max = round(max, 1)

    weather = {'TEMP': temp,
               'FEELS': feels,
               'DESC': description,
               'MIN': min,
               'MAX': max}
    
    return weather