from lib.plugins.Plugin import Plugin
from enum import IntEnum

import numpy as np
import random
import json


class Phase(IntEnum):
    START = 0
    JOIN = 1
    PLAY = 2


class Trivia(Plugin):
    def __init__(self, _):
        super().__init__("Trivia", ["create", "join", "start", "answer", "leaderboard", "end"])

        self.phase = Phase.START

        self.players = {}
        self.playing = 0
        self.pool = []

        self.questions = json.load(open("lib/plugins/Jeopardy/medium.json", "r"))
        self.question = {}

    def create(self, data):
        if self.phase == Phase.START:
            self.phase = Phase.JOIN
            msg = data["nick"] + " created a new game of Trivia. Do !join to join."
        else:
            msg = "There's another game going on."

        return msg

    def join(self, data):
        if self.phase >= Phase.JOIN:
            nick = data["nick"]

            if nick not in self.players.keys():
                self.players[nick] = 0
                self.pool.append(nick)
                msg = nick + " joined."
            else:
                msg = "You have already joined."
        else:
            msg = "You first need to create a new game. Do !create."

        return msg

    def start(self, _):
        if self.phase == Phase.JOIN:

            if len(self.players) >= 1:
                self.phase = Phase.PLAY

                # Shuffle the player's order
                random.shuffle(self.pool)

                msg = "The game is starting. Buckle up: " + ", ".join(self.pool)

                msg += "\n" + self.__ask()
            else:
                msg = "There are not enough players."

        elif self.phase > Phase.JOIN:
            msg = "The game has already started."
        else:
            msg = "You first need to create a new game. Do !create."

        return msg

    def __ask(self):
        nick = self.pool[self.playing]
        self.playing = (self.playing + 1) % len(self.pool)

        self.question = random.choice(self.questions)
        self.questions.remove(self.question)
        self.question["nick"] = nick

        return "%s: %s (%s): %s" % (
            self.question["nick"], 
            self.question["category"], 
            self.question["value"], 
            self.question["question"]
        )

    def answer(self, data):
        if self.phase < Phase.PLAY:
            return "You first need to start the game. Do !start."

        users_ans = " ".join(data["args"])

        if self.question["nick"] == data["nick"]:
            real_ans = self.question["answer"].lower()

            if valid_answer(real_ans, users_ans):
                self.players[nick] += int(self.question["value"][1:])

                msg = "Correct!"

                if real_ans != users_ans:
                    msg += " The precise answer was: " + self.question["answer"]
            else:
                msg = "Boooh. The correct answer was: " + self.question["answer"]

            msg += "\n" + self.__ask()
        else:
            msg = "The question wasn't addressed at you."

        return msg

    def leaderboard(self, _):
        msg = "Leaderboard:"
        order = 1

        for player, score in sorted(self.players.items(), key=lambda item: item[1], reverse=True):
            msg += "\n%d. %s: %d $" % (order, player, score)
            order += 1

        return msg

    def end(self, _):
        msg = self.leaderboard(_) + "\n"
        msg += "Alright, that'll be all."

        self.players = {}
        self.phase = Phase.START

        self.pool = []
        self.playing = 0

        return msg


def valid_answer(real_answer, given_answer):
    bound = 0 if len(real_answer) <= 3 else 1

    return given_answer in real_answer or real_answer in given_answer or \
           distance_in_bounds(real_answer, given_answer, bound)


def distance_in_bounds(s1, s2, bound):
    d = {}

    len_s1 = len(s1)
    len_s2 = len(s2)

    if abs(len_s1 - len_s2) > bound:
        return False

    for i in range(-1, len_s1 + 1):
        d[(i, -1)] = i+1

    for j in range(-1, len_s2 + 1):
        d[(-1, j)] = j+1

    for i in range(len_s1):
        for j in range(len_s2):
            cost = 0 if s1[i] == s2[j] else 1

            d[(i, j)] = min(
                d[(i-1, j-1)] + cost,  # Substitution
                d[(i-1, j)] + 1,  # Deletion
                d[(i, j-1)] + 1,  # Insertion
            )

            if i and j and s1[i] == s2[j-1] and s1[i-1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i-2, j-2] + cost)  # Transposition

    return d[len_s1 - 1, len_s2 - 1] <= bound
