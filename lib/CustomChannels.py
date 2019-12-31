import random
import lichess.api


class ChessUncensored(object):
    def __init__(self, data, bot):
        self.name = "##chess-uncensored"
        self.data = data
        self.bot = bot

    def rating(self, nick, mode=None):
        linick = self.lichess_username(nick)

        try:
            user = lichess.api.user(linick)
        except lichess.api.ApiHttpError:
            return "User not found."

        r = "<%s> " % linick

        if mode:
            r += "%s: %d" % (mode, user["perfs"][mode]["rating"])
        else:
            data = user["perfs"]

            for k in data.keys():
                r += "%s: %d, " % (k, data[k]["rating"])

            # Removes the last two characters from the string
            r = r[:-2]

        return r

    def tv(self, nick):
        return "https://lichess.org/@/%s/tv" % self.lichess_username(nick)

    def lichess_username(self, nick):
        lichess_usernames = self.data[self.name]["lichess_usernames"]
        return lichess_usernames[nick] if nick in lichess_usernames else nick
