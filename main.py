import json, inspect
from threading import Thread

from lib import CustomChannels
from lib.Bot import Bot

CONF_FILE_NAME = "conf.json"


def main():
    global bot, channels
    data = load_config()
    bot = Bot(data)

    # obj = getattr(CustomChannels, chan_name)(bot.data, bot)

    channels = {}

    for _, obj in inspect.getmembers(CustomChannels, inspect.isclass):
        try:
            channels[obj.name] = obj(bot.data, bot)
        except (AttributeError, TypeError):
            pass

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
    info = bot.listen()

    if not info:
        return

    nick, chan, cmd, args = info
    chan_name = chan.replace("#", "").title().replace("-", "")

    if find(["commands", cmd]):
        response = bot.form_msg(find(["commands", cmd]))
    elif find([chan, "commands", cmd]):
        response = bot.form_msg(find([chan, "commands", cmd]))
    elif find([chan, "actions", cmd]) and hasattr(CustomChannels, chan_name):
        void = bot.data[chan]["actions"][cmd]
        response = exec_command(channels[chan], void, args, nick)
    else:
        response = "The command you are trying to execute does not exist."

    bot.message(response, chan)


def exec_command(obj, func_name, args, nick):
    response = "That's not a valid command format."

    if hasattr(obj, func_name["function"]):
        func = getattr(obj, func_name["function"])

        if func_name["arguments"][0] <= len(args) <= func_name["arguments"][1]:
            response = func(*args)
        elif func_name["arguments"][0] == 1:
            response = func(nick)
        else:
            response = "The number of arguments is incorrect."

    return response


if __name__ == "__main__":
    main()
