from lib.plugins.Plugin import Plugin
from enum import IntEnum

import numpy as np
import urllib.request
import random
import json
import html


class Phase(IntEnum):
    START = 0
    JOIN = 1
    PLAY = 2


class Trivia(Plugin):
    def __init__(self, _):
        super().__init__("Trivia",
                         "Play a trivia game. cmds: !create; !join; !start; !answer <number>; !leaderboard; !leave; !end",
                         ["create", "join", "start", "answer", "leaderboard", "leave", "end"])

        self.__init()

    def __init(self):
        self.phase = Phase.START

        self.players = {}
        self.playing = 0
        self.pool = []

        self.questions = {}
        self.question = {}
    
    def __get_questions(self):
        """ Gets 50 random questions from opentdb and orders them by category. """

        url = urllib.request.urlopen("https://opentdb.com/api.php?amount=50")
        questions = json.loads(url.read().decode())["results"]

        for question in questions:
            category = question["category"].split(":")[0]

            if category in self.questions:
                self.questions[category].append(question)
            else:
                self.questions[category] = [question]
        
    def __get_question(self):
        """ Gets a random question from a random category. 
            This is done to avoid repeating categories many times. """
        
        while len(self.questions.keys()) < 5:
            self.__get_questions()

        category = random.choice(list(self.questions.keys()))

        self.question = random.choice(self.questions[category])
        self.questions[category].remove(self.question)

        if not self.questions[category]:
            self.questions.pop(category)

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

            if nick not in self.pool:
                self.players[nick] = {"questions": 0, "correct": 0}
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

        self.__get_question()

        # Adds the nick to the question to know who has to answer.
        self.question["nick"] = nick

        msg = "%s: %s (%s): %s" % (
            self.question["nick"], 
            self.question["category"], 
            self.question["difficulty"], 
            html.unescape(self.question["question"])
        )

        answers = self.question["incorrect_answers"]
        answers.append(self.question["correct_answer"])
        random.shuffle(answers)

        self.question["answers"] = answers

        msg += "\n"

        for i in range(len(answers)):
            msg += "%d. %s " % (i+1, html.unescape(answers[i]))

        return msg

    def answer(self, data):
        if self.phase < Phase.PLAY:
            return "You first need to start the game. Do !start."

        if self.question["nick"] != data["nick"]:
            return "The question wasn't addressed at you."

        # Input errors
        try:
            ans = int(data["args"][0])
        except IndexError:
            return "You didn't provide an argument."
        except ValueError:
            return "Your answer is not a number."

        if ans <= 0 or ans > len(self.question["answers"]):
            return "Not a valid answer."

        self.players[data["nick"]]["questions"] += 1

        # Answer check
        if self.question["answers"][ans-1] == self.question["correct_answer"]:
            self.players[data["nick"]]["correct"] += 1

            msg = "Correct!"
        else:
            msg = "Boooh. The correct answer was: " + html.unescape(self.question["correct_answer"])

        # Ask a new question
        msg += "\n" + self.__ask()

        return msg

    def leaderboard(self, _):
        msg = "Leaderboard:"
        order = 1

        for player, score in sorted(self.players.items(), key=lambda item: item[1]["correct"], reverse=True):
            msg += "\n%d. %s: %d  %.2f" % (order, player, score["correct"], score["correct"] / score["questions"])
            order += 1

        return msg

    def leave(self, data):
        if self.phase < Phase.PLAY:
            return "You first need to start the game. Do !start."

        if data["nick"] not in self.pool:
            return "You are not playing."

        self.pool.remove(data["nick"])

        if not self.pool:
            return self.end(data)

        self.playing %= len(self.pool)

        msg = "%s left." % data["nick"]

        if self.question["nick"] == data["nick"]:
            msg += '\n' + self.__ask()

        return msg
        

    def end(self, _):
        msg = self.leaderboard(_) + "\n"
        msg += "Alright, that'll be all."

        self.__init()

        return msg
