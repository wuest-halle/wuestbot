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

	"""Start and help message handler function

	Upon sending /start or /help all available commands are returned. 
	In the background the user's id is checked against the db and added,
	if there is no entry for the user yet.

	Arguments:
		message: telebot's message object
	"""

	u_id = message.from_user.id
	name = message.from_user.first_name
	is_bot = message.from_user.is_bot

	user = db_objects.User(u_id, name, is_bot)

	if not user.user_exists(u_id):
		user.add_user()

	with app.app_context():
		bot.send_message(chat_id=u_id, text=render_template('start.html', name=name), \
			parse_mode='html')

@bot.message_handler(commands=['next'])
def next_event(message):

	"""/next message handler function

	Upon sending the /next command the event's graphic and all available
	info from the db are returned.
	Artists are represented with hyperlinks. By pressing one of those,
	the artist message handler is triggered

	Arguments:
		message: telebot's message object
	"""

	u_id = message.from_user.id

	try:
		next_event = db_objects.get_next_event()
	except:
		return render_template('none.html')

	e_name = next_event.name
	date = next_event.date
	time = next_event.time
	admission = next_event.admission
	description = next_event.description
	location = next_event.location
	photo_id = os.path.join(img_dir, next_event.pic_id)
	
	atists_playing = db_objects.get_artists_event(e_name)

	with app.app_context():
		bot.send_photo(chat_id=u_id, photo=open(photo_id, 'rb'))
		bot.send_message(chat_id=u_id, text=render_template('next_event.html', \
			e_name=e_name, date=date, time=time, admission=admission, location=location, \
			description=description, artists=artists_playing), parse_mode='html')

@bot.message_handler(commands=['artist'])
def artist(message, name):

	"""/artist message handler function

	Upon sending the /artist command this function queries the db for 
	the corresponding artist and returns facts about it.

	Arguments:
		message: telebot's message object
		name: the artist's name
	"""

	u_id = message.user.id

	try:
		artist = db_objects.get_artist(name)
	except:
		return render_template('none.html')

	a_name = artist.name
	website = artist.website
	soundcloud = artist.soundcloud
	bandcamp = artist.bandcamp
	bio = artist.bio
	photo_id = artist.pic_id

	with app.app_context():
		bot.send_photo(chat_id=u_id, photo=open(photo_id, 'rb'))
		bot.send_message(chat_id=u_id, text=render_template('artist.html', \
			a_name=a_name, website=website, soundcloud=soundcloud, bandcamp=bandcamp, bio=bio), \
			parse_mode='html')

@bot.message_handler(func=lambda message: True)
def default(message):
	bot.reply_to(message, 'Sorry, message not understood')

bot.polling()