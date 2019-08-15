# WUESTBOT

This is a Telegram Bot for Halle based events team WUEST in the making. Check back later for more stuff. 

## Future Features

Future features will include:
- __Newsletter__: once you start a conversation with the bot, it will send you info on upcoming events (we'll keep it brief, I promise) 
- __Response__: ask it about past or future events or general info on WUEST, it'll answer

## Try it Out

To try this out on your own machine, clone the repo first. This is written in Python 3.7, so no guarantee it'll work in other versions. Start a terminal and change into the cloned folder. I recommend to create a venv then, so type:
``` bash
# create a new virtual environment
python -m venv <venvname>
# then activate it
source venv/bin/activate
```
substitute `<venvname>` with a name of your choice. Then install dependencies:
``` bash
pip install -r requirements.txt
```
Also you need to obtain your own token, 'cause I won't share mine.

That's all for now

## To Do:
- implement error checks in types.py/get_url(), if connection is down, telegram is down
- implement offset for latest messages
