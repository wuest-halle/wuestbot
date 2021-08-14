#!/usr/bin/env python3

import os
import logging
import time
from datetime import datetime

import flask
import telebot

from telebot import apihelper
from dotenv import load_dotenv
from traceback import print_exc

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN', '')
HOST = os.getenv('HOST', '')
PORT = os.getenv('PORT', '8443')

WEBHOOK_URL = f"https://{HOST}:{PORT}/bot{API_TOKEN}"

logging.basicConfig(filename='log.txt', encoding='utf-8', level=logging.DEBUG)

bot = telebot.TeleBot(API_TOKEN)

app = flask.Flask(__name__)

next_event = {
	"name": "ROUTINES 2021",
	"date": "SEP 12 - SEPT 25 2021",
	"description": """ROUTINES questions normality and everyday life in\
		its variety and repetitiveness by showcasing three works of individual\
		artists and groups in Spätshops spread across Halle. With each project\
		taking a different angle on the subject, it embeds critically engaging\
		art into our ordinary running for errands and opens an account to creative\
		work for everybody - outside of galleries and museums. Ultimately,\
		the exhibition engages in a dialogue with the subject which you are warmly\
		welcome to join into.
 		""",
	"artists": {
		"Asako Fujimoto, Maxime Lethelier": "",
		"Emma-Louise Meyer, Melanie Schulz": "",
		"Nancy Dewhurst": ""
	},
	"music": {}
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
			template = flask.render_template('start.html')
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

# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    logging.debug(time.now(), message)
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
		name = next_event["name"]
		date = next_event["date"]
		description = next_event["description"]
		artists = [artist for artist in next_event["artists"]]
	except Exception as e:
		logging.error(time.now(), e)
		print(e)

	try:
		bot.send_message(u_id, text=flask.render_template("next_event.html", 
			name=name, date=date, description=description, artists=artists), 
			parse_mode="html")
	except Exception as e:
		logging.error(time.now(), e)
		print(e)
	
	

#	with app.app_context():
#		try:
#			event = db_objects.Event.next()
#		except Exception as e:
#			pex(f"unable to retrieve next event: {e}")
#			send_template(u_id, flask.render_template('none.html'))
#			return
#
#		# Nothing scheduled.
#		if not event:
#			send_template(u_id, flask.render_template('404.html'))
#			return
#
#		# Send the picture, if possible.
#		# TODO: refactor, this should not throw an exception if the
#		# picture can't be found.
#		event.pic_id = os.path.join(img_dir, event.pic_id)
#		try:
#			bot.send_photo(
#				chat_id=u_id,
#				photo=open(event.pic_id, 'rb')
#			)
#		except Exception as e:
#			pex(f"Unable to send photo: {e}")
#
#		try:
#			send_template(
#				u_id,
#				flask.render_template(
#					'next_event.html',
#					e_name=event.name,
#					date=event.date,
#					time=event.time,
#					admission=event.admission,
#					location=event.location,
#					description=event.description,
#					artists=event.artists
#				)
#			)
#		except Exception as e:
#			pex(f"unable to send message: {e}")
#			send_template(u_id, flask.render_template('none.html'))
#