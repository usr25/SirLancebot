from lib.plugins.Plugin import Plugin

import requests, json


""" This class uses the open weather API to provide a simple msg with
    the weather in a city.
    Registration to get a valid API key is needed
"""
class Weather(Plugin):
    def __init__(self, data):
        super().__init__("Weather", ["weather"])
        self.data = data
        #TODO: Properly assign the key
        self.key = ""

    def key_is_valid(self):
        """ Ensure that the key is a 32-char hexadecimal string
        """
        try:
            m = map(lambda c : c >= '0' and c <= 'f', self.key)
            return len(self.key) == 32 and all(m)
        except:
            return False 

    def weather(self, data):
        """ Prints the weather information for the required city
        """

        if not self.key_is_valid():
            return "Ensure that the key has a valid format"

        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = data[0]
        complete_url = f"{base_url}appid={self.key}&q={city_name}" 

        response = requests.get(complete_url)
        res = response.json()

        return _parse_response(res)

def _to_celsius(temp):
    f = float(temp)
    f -= 274.15
    return "{:0.2f}".format(f)

def _parse_response(res):
    if res["cod"] == 200:

        temp = to_celsius(res["main"]["temp"])
        hum = res["main"]["humidity"]
        weather_main = res["weather"][0]["main"]
        weather_desc = res["weather"][0]["description"]

        return f"{temp}ºC {hum}% {weather_main} ({weather_desc})"
    else:
        if res["cod"] == 401:
            return "Key is invalid"
        return "No weather for that city or the key is invalid"
