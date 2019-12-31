from enum import IntEnum


class Phase(IntEnum):
    START = 0
    JOIN = 1
    PLAY = 2


class Trivia:
    def __init__(self):
        self.players = []
        self.phase = Phase.START

    def start(self):
        if self.phase == Phase.START:
            self.phase = Phase.JOIN
            msg = "Starting a new game of Trivia. To join do !join."
        else:
            msg = "There's another game going on."

        return msg

    def join(self, nick):
        if self.phase == Phase.JOIN:
            self.players.append(nick)
            msg = "%s joined" % nick
        elif self.phase > Phase.JOIN:
            msg = "The joining phase is over."
        else:
            msg = "You first need to start a new game."

        return msg

    def ready(self):
        if self.phase == Phase.JOIN:
            if len(self.players) > 1:
                self.phase = Phase.PLAY

                msg = "The game is starting. Buckle up: " + \
                      ", ".join([player for player in self.players])
            else:
                msg = "There are not enough players."
        elif self.phase > Phase.JOIN:
            msg = "The game has already started."
        else:
            msg = "You first need to start a new game."

        return msg

