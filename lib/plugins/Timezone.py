from lib.plugins.Plugin import Plugin

from datetime import datetime
import pytz


class Timezone(Plugin):
    def __init__(self, data):
        super().__init__("Timezone", ["time"])
        self.data = data

        self.timezones = pytz.all_timezones

    def time(self, data):
        city_name_iter = itertools.takewhile(lambda s: not s.startswith('-'), data["args"])
        city_name = " ".join(city_name_iter)

        for timezone in self.timezones:
            if city_name in timezone:
                time = datetime.now(pytz.timezone(timezone))
                return city_name + ": " + time.strftime('%H:%M:%S')

        return "No timezone for that city"
