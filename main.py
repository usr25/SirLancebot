from threading import Thread

import importlib
import json

from lib.Bot import Bot
from lib import plugins

CONF_FILE_NAME = "conf.json"

plugin_names = ["Trivia", "Lichess", "Timezone", "Weather", "Echo", "EightBall"]
plugins = []
name_to_plugin = {}

def main():
    global bot

    data = load_config()
    bot = Bot(data)

    for p_name in plugin_names:
        mod = importlib.import_module("lib.plugins." + p_name)
        plugins.append(getattr(mod, p_name)(data))
        name_to_plugin[p_name.lower()] = plugins[-1]

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

    if data["cmd"] == "h" or data["cmd"] == "help":
        msg = _help(data)
    else:
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


def _help(data):
    msg = ""

    not_recognized = []

    if data["args"] == None or data["args"] == []:
        msg = "The supported plugins are: "

        plugins_listed = ", ".join(plugin_names)
        msg += plugins_listed + " -> !h <plugin>"

    else:
        for name in data["args"]:
            lc_name = name.lower()
            try:
                msg += name_to_plugin[lc_name].helpmsg + '\n'
            except KeyError:
                not_recognized.append(lc_name)

        if not_recognized != []:
            msg += '(' + ",".join(not_recognized) + ") aren't recognized"

    return msg

if __name__ == "__main__":
    main()
