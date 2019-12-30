import random


class SomeChannel(object):
    def __init__(self, data, bot):
        self.name = "##some-channel"
        self.data = data
        self.bot = bot

    def whatof(self, arg=None):
        if arg in self.data[self.name]["whatof"]:
            return self.data[self.name]["whatof"][arg]
        else:
            return "There is no data for this user."
