import json
from threading import Thread

from lib import CustomChannels
from lib.Bot import Bot

CONF_FILE_NAME = "conf.json"


def main():
    global bot
    data = load_config()
    bot = Bot(data)

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

    nick, chan, cmd, arg = info
    chan_name = chan.replace("#", "").replace("-", "").title()

    if find(["commands", cmd]):
        response = bot.form_msg(find(["commands", cmd]), arg)
    elif find([chan, "commands", cmd]):
        response = bot.form_msg(find([chan, "commands", cmd]), arg)
    elif find([chan, "actions", cmd]) and hasattr(CustomChannels, chan_name):
        void = str(bot.data[chan]["actions"][cmd])
        obj = getattr(CustomChannels, chan_name)(bot.data, bot)
        response = exec_command(obj, void, arg)
    else:
        response = "The command you are trying to execute does not exist."

    bot.message(response, chan)


def exec_command(obj, func_name, arg):
    if hasattr(obj, func_name):
        func = getattr(obj, func_name)

        try:
            response = func(arg) if arg else func()
        except:
            pass

    else:
        response = "That's not a valid command format."

    return response


if __name__ == "__main__":
    main()
