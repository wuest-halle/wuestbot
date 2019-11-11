#!/usr/bin/env python

""" TO DO:
- proper error management if python can't parse token (applies to all html code)
- save known chat ids in file, so they dont have to restart every time
- how to push news to clients when new info is available?
- introduce error management for everything which isn't a proper command
- implement proper configuration, that knows all the paths and database 'n stuff
- implement exit MODE
- use a webhook instead of polling
- implement helpful help command
"""

""" KNOWN PITFALLS:
- always provide commands in a list, otherwise u get NoneType errors for
unknown commands, even when providing a default message (not sure y though)
"""

import os

from dotenv import load_dotenv
from flask import Flask, render_template
import telebot

from app.database import db_objects

# load env variables from .env
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

app = Flask(__name__)
bot = telebot.TeleBot(API_TOKEN)

img_dir = os.path.abspath('../bot/app/img')

@bot.message_handler(commands=['start', 'help'])
def start(message):

	u_id = message.from_user.id
	name = message.from_user.first_name
	is_bot = message.from_user.is_bot

	user = db_objects.User(u_id, name, is_bot)

	if not user.user_exists(u_id):
		user.add_user()

	with app.app_context():
		bot.send_message(chat_id=u_id, text=render_template('start.html', name=name), \
			parse_mode='html')

# returns flyer and info on the next event when user sends /next
@bot.message_handler(commands=['next'])
def next_event(message):

	u_id = message.from_user.id

	next_event = db_objects.get_next_event()

	e_name = next_event[1]
	date = next_event[2]
	time = next_event[3]
	admission = next_event[4]
	description = next_event[5]
	location = next_event[6]
	photo_id = os.path.join(img_dir, next_event[7])
	
	artists = db_objects.get_artists_event(e_name)

	with app.app_context():
		bot.send_photo(chat_id=u_id, photo=open(photo_id, 'rb'))
		bot.send_message(chat_id=u_id, text=render_template('next_event.html', \
			e_name=e_name, date=date, time=time, admission=admission, location=location, \
			description=description, artists=artists), parse_mode='html')

@bot.message_handler(commands=['message_to_all'])
def push_message_to_all(message):
	with open(os.path.join(template_dir, 'test.html'), 'r') as f:
		reply = f.read()
	uids = db.all_users()
	for uid in uids:
		print(uid[0])
		if (uid != 123456789) and (uid != 987654321):
			bot.send_message(chat_id=uid[0], text=reply, parse_mode='html')

@bot.message_handler(func=lambda message: True)
def default(message):
	bot.reply_to(message, 'Sorry, message not understood')

bot.polling()