from lib.plugins.Plugin import Plugin

import lichess.api


class Lichess(Plugin):
    def __init__(self, data):
        super().__init__("Lichess",
                         "Interact with Lichess. cmds: !rating <name> [category]; !tv <name>",
                         ["rating", "tv"])
        self.data = data

    def rating(self, data):
        user = data["args"][0] if data["args"] else data["nick"]
        mode = data["args"][1] if len(data["args"]) > 1 else None

        linick = self.__lichess_username(user)

        try:
            user = lichess.api.user(linick)
        except lichess.api.ApiHttpError:
            return "User not found."

        r = "<%s> " % linick

        if mode:
            if mode in user["perfs"]:
                r += "%s: %d" % (mode, user["perfs"][mode]["rating"])
            else:
                return "Incorrect mode."
        else:
            info = user["perfs"]

            for tc, rating in sorted(info.items(), key=lambda item: item[1]["rating"], reverse=True):
                r += "%s: %d, " % (tc, rating["rating"])

            r = r[:-2]

        return r

    def tv(self, data):
        user = data["args"][0] if data["args"] else data["nick"]
        return "https://lichess.org/@/%s/tv" % self.__lichess_username(user)

    def __lichess_username(self, nick):
        lichess_usernames = self.data[self.name]["lichess_usernames"]

        if nick in lichess_usernames:
            return lichess_usernames[nick]
        else:
            return nick
