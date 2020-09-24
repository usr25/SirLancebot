from lib.plugins.Plugin import Plugin

from datetime import datetime
import pytz


class Timezone(Plugin):
    def __init__(self, data):
        super().__init__("Timezone",
                         "Get current time in a city. cmd: !time <city>",
                         ["time"])
        self.data = data

        self.timezones = pytz.all_timezones

    def time(self, data):
        city = data["args"][0].title()

        for timezone in self.timezones:
            if city in timezone:
                time = datetime.now(pytz.timezone(timezone))
                return time.strftime('%H:%M:%S')

        return f"No timezone for {city}"
