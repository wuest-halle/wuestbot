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
import logging
import time 

from telebot import TeleBot, types
from dotenv import load_dotenv
from flask import Flask, render_template
from traceback import print_exc
import requests

from app.database import db_objects

# set logging
logging.basicConfig(filename=os.path.abspath('../log.txt'), level=logging.DEBUG)

# load env variables from .env file
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN', '')
ADMINS = os.getenv('ADMINS', '')
HOST = os.getenv('HOST', '')
PORT = os.getenv('PORT', '8443')
LISTEN_ON = os.getenv('LISTEN ON', '')
SSL_CERT = os.getenv('SSL_CERT', '')
SSL_PRIV = os.getenv('SSL_PRIV', '')

# define the URL to listen on
WEBHOOK_PATH = f"/{API_TOKEN}/"
WEBHOOK_URL = f"https://{HOST}:{PORT}/{API_TOKEN}/"

# create global instances of Flask and Telebot objcts
app = Flask(__name__)
bot = TeleBot(API_TOKEN)

img_dir = os.path.abspath('../bot/app/img')

def pex(msg):
	"""Log and error and print the traceback."""

	logging.error(msg)
	print_exc()

def get_admin_ids(env):
	"""Extracts admin IDs from a string.

	Admin IDs should be passed as environment variables like so:
	ADMINS=12345,812354,123013

	This function will split the string and return the IDs as a list. Empty
	parts of the string will be ignored.

	Args:
		env (str): A string containing the admin IDs, separated by commas.

	Returns:
		ids (list): A list of Telegram IDs of the Admins, or an empty list if
			parsing was unsuccessful.
	"""

	if not env or not isinstance(env, str):
		return []

	return [i for i in env.split(',') if i]

def send_template(u_id, template):
	"""Sends a template message via Telebot.

	The template must be given rendered.

	Args:
		template_name (str): The randered template to send.
	"""
	with app.app_context():
		try:
			bot.send_message(u_id,
				text=template,
				parse_mode='html'
			)
		except Exception as e:
			pex(f"unable to send message: {e}")

def keys(status):
	""" provides markup keyboards for the specified type of user,
	currently only admins

	Arguments:
		* status (str): status of the user requesting the keyboard,
		currently only 'admin' is allowed

	Returns:
		KeyboardMarkup object if proper status is defined
	"""

	if status == 'admin':
		keyb = types.ReplyKeyboardMarkup()
		opt_1 = types.KeyboardButton('a')
		opt_2 = types.KeyboardButton('z')
		keyb.add(opt_1, opt_2)
		return keyb

	else:
		logging.error("No proper status for keyboard defined")

def send_next_event(u_id):
	"""Sends the event with the highest eventID.

	Args:
		u_id (str): The chat ID to send the event to.
	"""
	with app.app_context():
		try:
			event = db_objects.Event.next()
		except Exception as e:
			pex(f"unable to retrieve next event: {e}")
			send_template(u_id, render_template('none.html'))
			return

		# Nothing scheduled.
		if not event:
			send_template(u_id, render_template('404.html'))
			return

		# Send the picture, if possible.
		# TODO: refactor, this should not throw an exception if the
		# picture can't be found.
		event.pic_id = os.path.join(img_dir, event.pic_id)
		try:
			bot.send_photo(
				chat_id=u_id,
				photo=open(event.pic_id, 'rb')
			)
		except Exception as e:
			pex(f"Unable to send photo: {e}")

		try:
			send_template(
				u_id,
				render_template(
					'next_event.html',
					e_name=event.name,
					date=event.date,
					time=event.time,
					admission=event.admission,
					location=event.location,
					description=event.description,
					artists=event.artists
				)
			)
		except Exception as e:
			pex(f"unable to send message: {e}")
			send_template(u_id, render_template('none.html'))

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

	if not user.exists_in_db(u_id):
		user.add_user()

	with app.app_context():
		send_template(u_id, render_template('start.html', name=name))

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

	with app.app_context():
		send_next_event(u_id)

@bot.message_handler(commands=['delete', 'cancel', 'remove'])
def delete(message):
	"""Deletes a user from the database."""
	u_id = message.from_user.id
	with app.app_context():
		user = db_objects.User.get_user(u_id)

		# Check if user exists.
		if not user:
			send_template(u_id, render_template('404.html'))
			return

		bye = ('We\'re sad to see you go! :(\n'
				'You have been deleted from our message list '
				'and will not be informed about future events. If you '
				'would like to subscribe again, please ping me with /start')

		# Delete user.
		if user.delete_from_db():
			send_template(u_id, bye)
		else:
			send_template(u_id, render_template('none.html'))

@bot.message_handler(commands=['push'])
def push(message):
	"""Sends a message to each user in the DB.

	Only 'admins' should be allowed to push, so a list of Telegram IDs
	can be provided via an environment variable:
	ADMINS=12345,3523423,8452349

	For now, this only sends the next event. In the future it can be
	extended by an argument to push a specific part such as:
		>>> /push next-event
		>>> /push event <name>
		>>> /push artist <name>
	"""

	caller_id = message.from_user.id
	with app.app_context():
		# Admin check. Templates during those checks will be sent to
		# the caller, not to the users.
		admins = get_admin_ids(ADMINS)
		if not admins:
			logging.error("No admins provided")
			send_template(caller_id, render_template('none.html'))
		if str(caller_id) not in admins:
			logging.warn(f"Not authorized: '{caller_id}' not in {admins}")
			send_template(caller_id, render_template('404.html'))

		# Retrieve all users and send a message to them.
		users = db_objects.User.all_in_db()
		if not users:
			send_template(caller_id, 'No users found.')
			return
		for user in users:
			logging.debug(f"sending to: {user.u_id}")
			send_template(user.u_id, render_template('intermediate.html'))

# @bot.message_handler(commands=['push_doc'])
@bot.message_handler(func=lambda message: message.caption == '/push_doc', content_types=['document'])
def push_doc(message):
	""" pushes content of a text document """

	u_id = message.from_user.id

	# check for user authorization
	if not authorize(u_id):
		bot.reply_to(message, "You cannot do that!")
		return

	# check mime type
	if message.document.mime_type != 'text/html':
		bot.reply_to(message, "Please provide an HTML formatted document")
		return

	# get text from message
	file_id = message.document.file_id
	file_info = bot.get_file(file_id)

	with requests.get(f'https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}') as resp:
		text = resp.content

	# send out to all users
	users = db_objects.User.all_in_db()
	if not users:
		send_template(u_id, 'No users found.')
		return
	for user in users:
		logging.debug(f"sending to: {user.u_id}")
		send_template(user.u_id, text)

# TODO: remove this comment when /artist is properly implemented
# @bot.message_handler(commands=['artist'])
def artist(message, name):

	"""/artist message handler function

	Upon sending the /artist command this function queries the db for
	the corresponding artist and returns facts about it.

	Arguments:
		message: telebot's message object
		name: the artist's name
	"""

	with app.app_context():

		u_id = message.from_user.id

		artist = db_objects.get_artist(name)
		if not artist:
			return render_template('404.html')

		a_name = artist.name
		website = artist.website
		soundcloud = artist.soundcloud
		bandcamp = artist.bandcamp
		bio = artist.bio
		photo_id = artist.pic_id


		try:
			bot.send_photo(chat_id=u_id, photo=open(photo_id, 'rb'))
		except Exception as e:
			logging.error(e)

		try:
			bot.send_message(chat_id=u_id, text=render_template('artist.html', \
				a_name=a_name, website=website, soundcloud=soundcloud, bandcamp=bandcamp, bio=bio), \
				parse_mode='html')
		except Exception as e:
			logging.error(e)
			return render_template('none.html')


def authorize(u_id):
	""" checks for admin authorization

	Arguments:
		* u_id (str): user's id

	Returns:
		* True, if user is admin
		* False otherwise
	"""

	with app.app_context():
		# Admin check. Templates during those checks will be sent to
		# the caller, not to the users.
		admins = get_admin_ids(ADMINS)
		if not admins:
			logging.error("No admins provided")
			send_template(u_id, render_template('none.html'))
			return False
		if str(u_id) not in admins:
			logging.warn(f"Not authorized: '{u_id}' not in {admins}")
			send_template(u_id, render_template('404.html'))
			return False

	return True

@bot.message_handler(func=lambda message: True)
def default(message):
	bot.reply_to(message, 'Sorry, message not understood')


# Process webhook calls
@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

time.sleep(2)

# Set webhook
bot.set_webhook(url=WEBHOOK_URL,
                certificate=open(SSL_CERT, 'r'))

# Start flask server
app.run(host=LISTEN_ON,
        port=PORT,
        ssl_context=(SSL_CERT, SSL_PRIV),
        debug=True)
