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

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN', '')
HOST = os.getenv('HOST', '')
PORT = os.getenv('PORT', '8443')

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
			accompanied by looped audio of the spot."""
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
			our world is in a crisis as with the pandemic we are still experiencing."""
		}
	},
	"interventions": {
		"SPAETI 007": {
			"date": "SEP 16 2021",
			"musicians": ""
		},
		"SCHERINS MARKT": {
			"date": "SEP 23 2021",
			"musicians": ""
		},
		"SCHWEMME": {
			"date": "SEP 25 2021",
			"musicians": ""
		}
	}, 
	"admission": "Free (donations appreciated)"
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

	# user = db_objects.User(u_id, name, is_bot)

	# if not user.exists_in_db(u_id):
	# 	user.add_user()

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
			reply_markup=artist_keyboard(),
			parse_mode="html")
	except Exception as e:
		print(e)

@bot.callback_query_handler(func=lambda call:True)
def send_info(call):
	""" returns info
	"""
	name = call.data

#	with app.context():
	if name in next_event["artists"]:
		try:
			artists = next_event["artists"]
			photo = artists[name]["photo"]
			description = artists[name]["description"]
			print(description)
			if description:
				try:
					with app.app_context():
						text=render_template(
							'artist.html',
							name=name,
							description=description)
						print(text)
				except Exception as e:
					print('cannot render template:', e)
				
				bot.edit_message_text(
					chat_id=call.message.chat.id,
					message_id=call.message.message_id, 
					text=text,
					parse_mode='html',
					reply_markup=artist_keyboard())
		except Exception as e:
			print(e)
	else:
		print("name not found in dict")

def artist_keyboard():
	""" constructs inline keyboard"""
		# construct the inline keyoard
	
	try:
		inline = types.InlineKeyboardMarkup(row_width=1)
		btn1 = types.InlineKeyboardButton(
			text='Asako Fujimoto, Maxime Lethelier', 
			callback_data='Asako Fujimoto, Maxime Lethelier')
		btn2 = types.InlineKeyboardButton(
			text='Nancy Dewhurst', 
			callback_data='Nancy Dewhurst')
#		btn4 = types.InlineKeyboardButton(
#			text='Go Back', 
#			callback_data='Go Back')
		inline.add(btn1, btn2)
	except Exception as e:
		print('cannot compile keyboard:', e)

	return inline