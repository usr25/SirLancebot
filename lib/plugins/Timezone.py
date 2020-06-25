from lib.plugins.Plugin import Plugin

from datetime import datetime
import pytz


class Timezone(Plugin):
    def __init__(self, data):
        super().__init__("Timezone", ["time"])
        self.data = data

        self.timezones = pytz.all_timezones

    def time(self, data):
        country = data["args"][0].title()

        for timezone in self.timezones:
            if country in timezone:
                time = datetime.now(pytz.timezone(timezone))
                return country + ": " + time.strftime('%H:%M:%S')

        return "No timezone for that city"
