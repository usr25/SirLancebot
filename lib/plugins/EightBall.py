from lib.plugins.Plugin import Plugin
import random

sentences = ["It is certain","It is decidedly so", "Without a doubt", "Yes – definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes","Reply hazy, try again","Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","My sources say no","Outlook not so good","Very doubtful"]

class EightBall(Plugin):
    def __init__(self, data):
        super().__init__("EightBall",
                         "Prints a random answer. cmd: !eball (msg)",
                         ["eball"])
        self.data = data


    def eball(self, data):
        return random.choice(sentences)