# SirLancebot

A simple python bot. It's intended to be easy for plugins.
The bot consists mostly of main.py and lib/Bot.py.
To add code for a new channel just add an object to lib/CustomChannels.py following the example.

## Code

The code is structured in three main files.
1. **Bot.py**: Handles sockets and connections.
2. **main.py**: Interacts with Bot.py and links all plugins together.
3. **CustomChannels.py**: Deals with plugins.

### Plugins
A plugin specifies the actions the bot should be able to perform in the channel it's named after.

```
class ChannelName(object):
    def __init__(self, data, bot):
        self.name = "#channel_name"
        self.data = data
        self.bot = bot
        
    def shout(self, arg=None):
        """ An example of an action, it should return a response. The arg is optional. """
        if arg:
            return "HELLO %s!" % arg.upper()
        
        return "HELLO!"
```

Actions should only be used for answers that need some kind of computation. If it is 
a static response it should be added to the conf.json following the structure below:

```
{
    "#channel_name": {
        "commands": {
            "hello": "Hello"  # Answers `Hello` when someone executes `?hello`.
        },
        "actions": {
            "shout": "shout"  # Points the command `?shout` to the function `shout`.
        }
    }
}
```

## Config file

This file is not included in the repository and must be added. Each channel should have 
an entry as shown below. 

```
{
    'conf' = {
        "irc": str(),       # IRC's address
        "port": int(),      # IRC's port
        "nick": str(),      # Bot's nick
        "user": str(),      # Bot's username
        "real": str(),      # Bot's realname
        "pass": str()       # Bot's password
        "chans": [str()],   # Channels to connect to
    }
}
```
