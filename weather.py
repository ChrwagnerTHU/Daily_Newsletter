import pyowm
import os
import json

def get_weather (, __location__, location):
    weather = ""

    with open (__location__ + "/ressource/config.json", "r") as f:
        config = json.load(f)
        api_key = config['App']['WEATHER_API']
        f.close()
    
    owm = pyowm.OWM(api_key)
    weather_mgr = owm.weather_manager()
    observation = weather_mgr.weather_at_place(location)

    print(observation)


    return weather

if __m