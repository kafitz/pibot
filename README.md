### Pibot
Pibot is the IRC outputer for the [logbot](https://github.com/kafitz/logbot) project. Pibot 
is a stripped down version of [phenny](http://inamidst.com/phenny/) that receives messages 
using redis' pubsub as JSON. The messages are sent via a channel named ```irc_msg``` in the 
format:
```{'type': 'message', 'data': {'channel': #ircchannel, 'text': 'abcde'} }

#### Setup
1. Pibot simply requires the redis python package:
```pip install redis```
2. Run ```python pibot.py``` to generate an initial config for pibot.
3. Edit the config in the ```configs``` folder and run ```python pibot.py``` again to begin the bot.
Run logbot or other redis messenger to begin IRC output in whichever channels are joined.

#### Notes
