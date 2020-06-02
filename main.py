from threading import Thread

import importlib
import json

from lib.Bot import Bot
from lib import plugins

CONF_FILE_NAME = "conf.json"

plugins = ["Trivia", "Lichess", "Timezone"]


def main():
    global bot

    data = load_config()
    bot = Bot(data)

    for i in range(len(plugins)):
        mod = importlib.import_module("lib.plugins." + plugins[i])
        plugins[i] = getattr(mod, plugins[i])(data)

    # Input written in the prompt would be sent as bot's messages
    Thread(target=chat).start()

    print("[+] bot is up and running")
    print(bot.conf["chans"][0])

    while True:
        listen()


def load_config():
    f = open(CONF_FILE_NAME, 'r')
    data = json.load(f)
    return data


def chat():
    while True:
        bot.message(input(), bot.conf["chans"][0])


def find(path):
    data = bot.data

    for subpath in path:
        if subpath not in data:
            return False

        data = data[subpath]

    return data


def listen():
    data = bot.listen()

    if not data:
        return

    msg = "The command you are trying to execute does not exist."

    for plugin in plugins:
        if data["cmd"] in plugin.cmds:
            msg = exec_cmd(plugin, data)

    bot.message(data["chan"], msg)


def exec_cmd(plugin, data):
    msg = "That's not a valid command format."

    func = getattr(plugin, data["cmd"])

    #try:
    msg = func(data)
    #except ValueError:
    #    msg = "The number of arguments is incorrect."

    return msg


if __name__ == "__main__":
    main()
