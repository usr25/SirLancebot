# SirLancebot

A simple python bot. It's intended to be easy for plugins.
The bot consists mainly of main.py and lib/Bot.py.
To add code for a new plugin just add your code to the plugins folder.

## Code

The code is structured in three main files.
1. **Bot.py**: Handles sockets and connections.
2. **main.py**: Interacts with Bot.py and links all plugins together.
3. **Plugin.py**: States the main structure every plugin should follow.

### Plugins
A plugin specifies a series of actions to be performed in any of the channels the bot is in.
Initalize your plugin with its name and the list of commands it handles. The plugin's commands should have a function named after them that takes in a dictionary data and returns a message.

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
        "weather_key": str()# Key for the weather api openweathermap
    }
}
```
