import random
import lichess.api


class ChessUncensored(object):
    def __init__(self, data, bot):
        self.name = "##chess-uncensored"
        self.data = data
        self.bot = bot

    def rating(self, nick, mode=None):
        try:
            user = lichess.api.user(nick)
        except lichess.api.ApiHttpError:
            return "User not found."

        r = str()

        if mode:
            r = user["perfs"][mode]["rating"]
        else:
            data = user["perfs"]

            for k in data.keys():
                r += "%s: %d, " % (k, data[k]["rating"])

            # Removes the last two characters from the string
            r = r[:-2]

        return r
