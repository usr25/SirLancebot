from lib.plugins.Plugin import Plugin

import requests
import itertools


class Weather(Plugin):
    """ This class uses the open weather API to provide a city's weather.
        Registration to get a valid API key is needed. """
    def __init__(self, data):
        super().__init__("Weather",
                         "Weather for a city. cmd: !weather <city>" ,
                         ["weather"])

        self.data = data
        self.key = self.data[self.name]["key"]

    def key_is_valid(self):
        """ Ensure that the key is a 32-char hexadecimal string. """
        
        try:
            m = map(lambda c : '0' <= c <= 'f', self.key)
            return len(self.key) == 32 and all(m)
        except:
            return False 

    def weather(self, data):
        """ Prints the weather information for the required city. """

        if not self.key_is_valid():
            return "(DEVELOPER) Ensure that the API key has a valid format"

        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name_iter = itertools.takewhile(lambda s: not s.startswith('-'), data["args"])
        city_name = " ".join(city_name_iter)

        complete_url = base_url + "appid=" + self.key + "&q=" + city_name

        response = requests.get(complete_url)
        
        # Print res to see the possible options
        res = response.json()

        return _parse_response(res)


def _to_celsius(temp):
    f = float(temp)
    f -= 274.15
    return "{:0.2f}".format(f)


def _parse_response(res):
    if res["cod"] == 200:
        temp = _to_celsius(res["main"]["temp"])
        feels_like = _to_celsius(res["main"]["feels_like"])
        hum = res["main"]["humidity"]
        weather_desc = res["weather"][0]["description"]

        return "%sºC; feels like: %sºC; %s%% (%s)" % (temp, feels_like, hum, weather_desc)
    elif res["cod"] == 401:
        return "Key is not accepted by openweathermap.com"
        
    return "No weather for that city"
