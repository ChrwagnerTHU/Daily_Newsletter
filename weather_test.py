import pyowm
import os
import json

def get_weather (location):
    weather = ""
    __location__ = os.path.dirname(os.path.abspath(__file__))

    with open (__location__ + "/ressource/config.json", "r") as f:
        config = json.load(f)
        api_key = config['App']['WEATHER_API']
        f.close()
    
    owm = pyowm.OWM(api_key)
    weather_mgr = owm.weather_manager()
    observation = weather_mgr.weather_at_place(location)

    print(observation)
    return weather

weather = get_weather("Ulm")