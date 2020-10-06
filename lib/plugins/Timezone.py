from lib.plugins.Plugin import Plugin

from datetime import datetime
import pytz
import itertools


class Timezone(Plugin):
    def __init__(self, data):
        super().__init__("Timezone",
                         "Get current time in a city. cmd: !time <city>",
                         ["time"])
        self.data = data

        self.timezones = pytz.all_timezones

    def time(self, data):
        city_name = " ".join(arg.title() for arg in data["args"])
        city_code = city_name.replace(" ", "_")

        for timezone in self.timezones:
            if city_code in timezone:
                time = datetime.now(pytz.timezone(timezone))
                return city_name + ": " + time.strftime('%H:%M:%S')
        
        return "No timezone for " + city_name
