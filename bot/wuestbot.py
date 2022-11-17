#!/usr/bin/env python3

import os
import logging
import time
from datetime import datetime

import flask
import telebot

from telebot import apihelper, types
from dotenv import load_dotenv
from traceback import print_exc
from flask import render_template

from app.database import db_objects

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN', '')
HOST = os.getenv('HOST', '')
PORT = os.getenv('PORT', '8443')
ADMINS = os.getenv('ADMINS')

WEBHOOK_URL = f"https://{HOST}:{PORT}/bot{API_TOKEN}"

logging.basicConfig(filename='log.txt', encoding='utf-8', level=logging.DEBUG)

bot = telebot.TeleBot(API_TOKEN)

app = flask.Flask(__name__)

next_event = {
	"photo": "wuest_strives_general.png",
	"name": "WUEST STRIVES",
	"date": "NOV 10",
	"description": """Come to join WUEST on a boat""",
	"artists": {
		"Somali Vendetta": {
			"photo": "",
			"description": """somali vendetta (they/them/king) is a queer Somali DJ\
			based in Leipzig. The genres of music they play are rather eclectic and\
			depend on the vibe. It ranges from Amapiano to Afrobeats or UK Garage\
			to UK Bass and Techno. The selections are good because they are made for\
			dancing.""",
			"website": "https://soundcloud.com/somalivendetta"
		},
		".neelie aka colluvisol": {
			"photo": "",
			"description": """neelie. places a strong focus on contemporary web culture\
			in different areas of her work - be it while playing records or pushing\
			her project called oh mochi.\
			Her sound got influenced by beat tapes, vaporwave, and low-fidelity hip hop\
			and takes its twists with UK bass and her deep love for Soundsystem culture.\
			Besides curating and playing events, neelie. aka colluvisol is part of\
			II.Reihe for Tarmac Festival and you can hear her mixes in shows on Bristol\
			Radio Noods, London-based Threads, or Frankfurts EOS Radio, to name some.
			""",
			"website": "https://soundcloud.com/neelie-3"
		}, 
		"JLULULU": {
			"photo": "",
			"description": """JLULULU [dʒeɪ lululu] creates a coupling of post-club\
			enigmas and percussive, quirky art pop questioning contemporary restrictions.\
			Get involved in a wide dynamic range of deconstructed bangers and shaky beats\
			– presented with a fresh provocative streak.""",
			"website": "https://soundcloud.com/jlululu"
		},
		"Sirko Mueller": {
			"photo": "",
			"description": """One half of the Tokomak Records company and former a main\
			founding member of Tokomak. He is well known for his diversity in music, where\
			he draws many influences from tha big D(etroit). Several high-quality releases\
			for some exciting labels like the well-known Milnor Modern imprint or Rewired\
			Records have proven his skills and taste. A master of funky rhythm patterns\
			without losing sight of the deepness and power of his productions. """,
			"website": "https://soundcloud.com/sirko-mueller "
		}
	},
	"admission": "8€"
}


# Process webhook calls
@app.route(f'/bot', methods=['POST'])
def webhook():
	""" default route to process webhook updates

	The function takes POST requests to the url and processes the JSON string

	returns:
		none

	"""
	if flask.request.headers.get('content-type') == 'application/json':
		json_string = flask.request.get_data().decode('utf-8')
		update = telebot.types.Update.de_json(json_string)
		bot.process_new_updates([update])
		return "!", 200
	else:
		flask.abort(403)

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
		try:
			template = render_template('start.html')
			send_template(u_id, template)
		except:
			logging.error('cannot send template:', message.text)

@bot.message_handler(commands=['next'])
def next(message):

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
		with app.app_context():
			send_next_event(u_id)
	except Exception as e:
			print(e)

@bot.message_handler(commands=['artist'])
def send_artist(message):
	""" send info and picture of artist to requesting user

	args:
	    * u_id (str): user id who requested the info
	    * name (str): name of the artist
	"""

	bot.reply_to(message, 'hi')

@bot.message_handler(commands=['delete', 'cancel', 'remove'])
def delete(message):
	"""Deletes a user from the database."""
	error = "Sorry, something went wrong..."
	with app.app_context():
		user = db_objects.User.get_user(message.from_user.id)

		# Check if user exists.
		if not user:
			bot.reply_to(message, error)
			return

		bye = ('We\'re sad to see you go! :(\n'
				'You have been deleted from our message list '
				'and will not be informed about future events. If you '
				'would like to subscribe again, please ping me with /start')
		# Delete user.
		if user.delete_from_db():
			bot.reply_to(message, bye)
		else:
			bot.reply_to(message, error)

@bot.message_handler(commands=['push'])
def push_event(message):
	""" push the next event message to users in db"""
	caller_id = message.from_user.id
	admins = get_admin_ids(ADMINS) 
	
	if caller_id not in admins:
		bot.reply_to(message, "Sorry, you are not allowed to do this")
	
	else:
		try:
			users = db_objects.User.all_in_db()
			for user in users:
				try:
					photo = open(f"""./app/img/wuest_strives_general.png""", "rb")
					bot.send_photo(user.u_id, photo)
					with app.app_context():
						bot.send_next_event()
				except Exception as e:
					logging.error(f"pushing to user {user.u_id} not possible: ", e)
		except Exception as e:
			logging.error("pushing not possible: ", e)

#@bot.message_handler(commands=['location'])
#def location(message):
#	"""
#	"""
#	bot.reply_to(message, message)
#	text = message.text
#	name = text - 'location '
#	try:
#		lat = next_event["locations"]["SPÄTI TO GO"]["lat"]
#		lon = next_event["locations"]["SPÄTI TO GO"]["lon"]
#		print(lat, lon)
#	except Exception as e:
#		print(e)
#	bot.send_location(message.from_user.id, lat, lon)

# Handle all other messages
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, """Sorry, I don't know this :( try /help to
    see what I can understand""")

def send_template(u_id, template):
	"""Sends a template message via Telebot.
	The template must be given rendered.
	Args:
		template_name (str): The rendered template to send.
	"""
	try:
		bot.send_message(u_id,
			text=template,
			parse_mode='html'
		)
	except Exception as e:
		pex(f"unable to send message: {e}")

def pex(msg):
	"""Log and error and print the traceback."""

	logging.error(msg)
	print_exc()

def send_next_event(u_id):
	"""Sends the event with the highest eventID.
	Args:
		u_id (str): The chat ID to send the event to.
	"""

	keys = keyboards()

	try:
		photo = open(f"""./app/img/{next_event["photo"]}""", "rb")
		name = next_event["name"]
		date = next_event["date"]
		description = next_event["description"]
		artists = [artist for artist in next_event["artists"]]
		admission = next_event["admission"]
	except Exception as e:
		logging.error(e)
		print('assignment error', e)

	try:
		bot.send_photo(u_id, photo)
	except Exception as e:
		print('picture error', e)
	
	try:
		bot.send_message(
			u_id, 
			text=render_template(
				"next_event.html", 
				name=name, 
				date=date, 
				description=description, 
				artists=artists,
				admission=admission), 
			reply_markup=keys[1],
			parse_mode="html")
	except Exception as e:
		print('sending error', e)

@bot.callback_query_handler(func=lambda call:True)
def send_info(call):
	""" returns info
	"""
	data = call.data
	keys = keyboards()

	if data == "Artists":
		bot.edit_message_text(
			chat_id=call.message.chat.id,
			message_id=call.message.message_id,
			text="Click on the buttons below to get more info on artists", 
			parse_mode='html',
			reply_markup=keys[0])
	
	if data == "Interventions":
		bot.edit_message_text(
			chat_id=call.message.chat.id,
			message_id=call.message.message_id, 
			text="Click on the buttons below to get more info on what's happening at each location",
			parse_mode='html',
			reply_markup=keys[1])

	if data in next_event["artists"]:
		try:
			artists = next_event["artists"]
			photo = artists[data]["photo"]
			description = artists[data]["description"]
			if description:
				try:
					with app.app_context():
						text=render_template(
							'artist.html',
							name=data,
							description=description)
				except Exception as e:
					print('cannot render template:', e)				
				bot.edit_message_text(
					chat_id=call.message.chat.id,
					message_id=call.message.message_id, 
					text=text,
					parse_mode='html',
					reply_markup=keys[0])
		except Exception as e:
			print(e)

	if data in next_event["interventions"]:
		try:
			interventions = next_event["interventions"]
			description = interventions[data]["description"]
			date = interventions[data]["date"]
			lat = interventions[data]["lat"]
			lon = interventions[data]["lon"]
			location = interventions[data]["location"]
			if description:
				try:
					with app.app_context():
						text=render_template(
							'interventions.html',
							name=data,
							date=date,
							description=description,
							location=location)
				except Exception as e:
					print('cannot render template:', e)				
				bot.edit_message_text(
					chat_id=call.message.chat.id,
					message_id=call.message.message_id, 
					text=text,
					parse_mode='html',
					reply_markup=keys[1])
		except Exception as e:
			print(e)

	
	if data == "Go Back":
		try:
			name = next_event["name"]
			date = next_event["date"]
			description = next_event["description"]
			artists = [artist for artist in next_event["artists"]]
			interventions = [intervention for intervention in next_event["interventions"]]
			admission = next_event["admission"]
			if description:
				try:
					with app.app_context():
						text = render_template(
							"next_event.html", 
							name=data, 
							date=date, 
							description=description, 
							artists=artists,
							interventions=interventions, 
							admission=admission)
				except Exception as e:
					print('cannot render template:', e)
				
				bot.edit_message_text(
					chat_id=call.message.chat.id,
					message_id=call.message.message_id, 
					text=text,
					parse_mode='html',
					reply_markup=keys[2])
		except Exception as e:
			print(e)
	else:
		print("name not found in dict")

def keyboards():
	""" constructs inline keyboard"""
	
	try:
		artists = types.InlineKeyboardMarkup(row_width=1)
		btn1 = types.InlineKeyboardButton(
			text='Somali Vendetta', 
			callback_data='Somali Vendetta')
		btn2 = types.InlineKeyboardButton(
			text='.neelie aka colluvisol', 
			callback_data='.neelie aka colluvisol')
		btn3 = types.InlineKeyboardButton(
			text='JLULULU', 
			callback_data='JLULULU')
		btn4 = types.InlineKeyboardButton(
			text='SIRKO MUELLER', 
			callback_data='SIRKO MUELLER')
		btn5 = types.InlineKeyboardButton(
			text='Go Back',
			callback_data='Go Back')
		artists.add(btn1, btn2, btn3, btn4, btn5)
	except Exception as e:
		print('cannot compile artists keyboard:', e)
	
	try:
		overview = types.InlineKeyboardMarkup(row_width=1)
		btn9 = types.InlineKeyboardButton(
			text='Artists', 
			callback_data='Artists')
		overview.add(btn9)
	except Exception as e:
		print('cannot compile artists keyboard:', e)


	return [artists, overview]

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

	return [int(i) for i in env.split(',') if i]
