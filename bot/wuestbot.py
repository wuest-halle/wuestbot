#!/usr/bin/env python3

import os
import logging
import time
from datetime import datetime

import flask
import telebot

from telebot import apihelper

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN', '')

HOST = os.getenv('HOST', '')
PORT = os.getenv('PORT', '8443')
# WEBHOOK_LISTEN = os.getenv('LISTEN_ON', '')
# WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
# WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

WEBHOOK_URL = f"https://{HOST}:{PORT}/bot{API_TOKEN}"

logging.basicConfig(filename='log.txt', encoding='utf-8', level=logging.DEBUG)

bot = telebot.TeleBot(API_TOKEN)

app = flask.Flask(__name__)


# Empty webserver index, return nothing, just http 200
#@app.route('/', methods=['GET', 'HEAD'])
#def index():
#    return ''


# Process webhook calls
@app.route(f'/bot', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, message.text)

# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


# Remove webhook, it fails sometimes the set if there is a previous webhook
# bot.remove_webhook()

# time.sleep(1)
# 
# # Set webhook
# bot.set_webhook(url=WEBHOOK_URL)

# Start flask server
# app.run(host=WEBHOOK_LISTEN,
#        port=WEBHOOK_PORT,
#        debug=True)