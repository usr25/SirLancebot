from lib.plugins.Plugin import Plugin

from datetime import datetime
import pytz
import itertools


class Timezone(Plugin):
    def __init__(self, data):
        super().__init__("Timezone", ["time"])
        self.data = data

        self.timezones = pytz.all_timezones

    def time(self, data):
        city_name = " ".join(arg.title() for arg in data["args"])

        for timezone in self.timezones:
            if city_name in timezone:
                time = datetime.now(pytz.timezone(timezone))
                return city_name + ": " + time.strftime('%H:%M:%S')

        return "No timezone for that city"
