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
	"photo": "routines_2021_general.png",
	"name": "ROUTINES 2021",
	"date": "SEP 10 - 25",
	"description": """ROUTINES questions normality and everyday life in\
	its variety and repetitiveness by showcasing three works of individual\
	artists and groups in Spätshops spread across Halle. With each project\
	taking a different angle on the subject, it embeds critically engaging\
	art into our ordinary running for errands and opens an account to creative\
	work for everybody - outside of galleries and museums. Ultimately,\
	the exhibition engages in a dialogue with the subject which you are warmly\
	welcome to join into.""",
	"artists": {
		"Asako Fujimoto, Maxime Lethelier": {
			"photo": "",
			"description": """Asako Fujimoto is a sound artist and musician\
			interested in sonic representations of nature as well as algorithmic\
			composition. Maxime Lethelier is a mixed media artist who works\
			on representations of modern society.\n
			Their work HU/AU Bacus is an audiovisual encounter with metadata\
			of daily human movement collected by the market. Eventually, this\
			data would become more valuable than gold or steel. The installation\
			shows the flow of customers in relation to stock market prices\
			accompanied by looped audio of the spot.""",
			"website": ""
		},
		"Rose Magee": {
			"photo": "",
			"description": """Rose Magee’s work is her impression of reality,\
			offering room for opinion and interpretation. She aims to create\
			space for political discussion through her creative output.\n
			The work she has devised for ROUTINES critically engages with\
			the repercussions of our grocery shopping pattern. Through using\
			recycled materials she asks for consciousness around packaging and\
			waste, which became even more impactful on our environment through\
			people mass-acquiring supplies during the pandemic. Watch out of\
			her plastics spread throughout the shop.
			""",
			"website": ""
		}, 
		"Nancy Dewhurst": {
			"photo": "",
			"description": """Nancy Dewhurst’s work focuses on participatory pieces,\
			playful encounters to research-based topics. She is interested in\
			systems and the way these might change in the future.\n
			Left-Hand Turn is a collection of giant shells - press them to your\
			ear and you may hear their daily doing as you would hear the ocean\
			through seashell resonance. It questions how we deal with the environment\
			for our own pleasure and the need to keep up with routines even though\
			our world is in a crisis as with the pandemic we are still experiencing.""",
			"website": ""
		}
	},
	"interventions": {
		"Späti 007": {
			"date": "SEP 16 2021",
			"description": """DJ Residue’s stripped down utilitarianism will be framed via Asako’s\
			and Maxime’s piece on the data economy. His live set feels like an antidote\
			of sorts to the shiny appearance of city centers in late capitalism. The\
			evening will be started off with sure-shot electronics by DJ Lara Palmer.""",
			"lat": "",
			"lon": "",
			"location": "https://www.openstreetmap.org/node/890216896#map=19/51.48624/11.97503"
		},
		"Scherins Markt": {
			"date": "SEP 23 2021",
			"description": """alobhe’s overdriven tenderness will be visible amidst\
			Rose’s warped wrappings of our everyday occupations. Brutal and hell-bent,\
			her music is as broken as our society became in 2020. She will play live.\
			Jlululu gets you up to operating temperature with two hours of red hot\
			post club music from the digital decks.""",
			"lat": "",
			"lon": "",
			"location": "https://www.openstreetmap.org/node/3870926327#map=19/51.50152/11.95545"
		},
		"Schwemme": {
			"date": "SEP 25 2021",
			"description": """We will draw ROUTINES to a conclusion at Schwemme.\
			Ana Bogner’s liberated neo-acoustics draw influence from many musics.\
			The style of her live sets could be described as collected and iterative.\
			Iterative is also John Horton’s approach to “The Sum Of Its Parts -\
			the auditive documentation of ROUTINES. He will present live snippets\
			recorded throughout the whole of the event - layered and morphed. Both\
			live artists will receive DJ support from Vanessa Bettina who present\
			collected oddities, outliers of what we routinely hear. WUEST’s own GREGOR.\
			will connect the dots with records from all spheres of electronics.""",
			"lat": "",
			"lon": "",
			"location": "https://www.openstreetmap.org/way/181008066"
		}
	}, 
	"admission": "Free (donations appreciated)",
	"locations": {
		"SPÄTI TO GO": {
			"lat":"51.4902",
			"lon":"11.9659",
		},
		"SCHERINS MARKT": {
			"lat":"",
			"lon":"",
		},
		"SPÄTI 007": {
			"lat":"",
			"lon":"",
		},
		"SCHWEMME": {
			"lat":"",
			"lon":"",
		}
	}
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

	with app.app_context():
		send_next_event(u_id)

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
					photo = open(f"""./app/img/routines_2021_events.jpg""", "rb")
					bot.send_photo(user.u_id, photo)
					with app.app_context():
						bot.send_message(
							user.u_id, 
							text=render_template("push.html"),
							parse_mode='html')
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
		interventions = [intervention for intervention in next_event["interventions"]]
		admission = next_event["admission"]
	except Exception as e:
		logging.error(time.now(), e)
		print(e)

	try:
		bot.send_photo(u_id, photo)
	except Exception as e:
		print(e)
	
	try:
		bot.send_message(
			u_id, 
			text=render_template(
				"next_event.html", 
				name=name, 
				date=date, 
				description=description, 
				artists=artists,
				interventions=interventions, 
				admission=admission), 
			reply_markup=keys[2],
			parse_mode="html")
	except Exception as e:
		print(e)

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
			text='Asako Fujimoto, Maxime Lethelier', 
			callback_data='Asako Fujimoto, Maxime Lethelier')
		btn2 = types.InlineKeyboardButton(
			text='Nancy Dewhurst', 
			callback_data='Nancy Dewhurst')
		btn3 = types.InlineKeyboardButton(
			text='Rose Magee', 
			callback_data='Rose Magee')
		btn4 = types.InlineKeyboardButton(
			text='Go Back',
			callback_data='Go Back')
		artists.add(btn1, btn2, btn3, btn4)
	except Exception as e:
		print('cannot compile artists keyboard:', e)

	try:
		locations = types.InlineKeyboardMarkup(row_width=1)
		btn5 = types.InlineKeyboardButton(
			text='Späti 007', 
			callback_data='Späti 007')
		btn6 = types.InlineKeyboardButton(
			text='Scherins Markt', 
			callback_data='Scherins Markt')
		btn7 = types.InlineKeyboardButton(
			text='Schwemme', 
			callback_data='Schwemme')
		btn8 = types.InlineKeyboardButton(
			text='Go Back',
			callback_data='Go Back')
		locations.add(btn5, btn6, btn7, btn8)
	except Exception as e:
		print('cannot compile locations keyboard:', e)	
	
	try:
		overview = types.InlineKeyboardMarkup(row_width=1)
		btn9 = types.InlineKeyboardButton(
			text='Artists', 
			callback_data='Artists')
		btn10 = types.InlineKeyboardButton(
			text='Interventions', 
			callback_data='Interventions')
		overview.add(btn9, btn10)
	except Exception as e:
		print('cannot compile artists keyboard:', e)


	return [artists, locations, overview]

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
