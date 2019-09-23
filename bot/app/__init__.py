#!/usr/bin/env python

import os

from dotenv import load_dotenv
import telebot

from flask import Flask, render_template

app = Flask(__name__)

# load env variables from .env
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

template_dir = os.path.abspath('../bot/templates')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['test'])
def test(message):
	with open(os.path.join(template_dir, 'test.html'), 'r') as f:
		reply = f.read()
	bot.send_message(message.chat.id, reply, parse_mode='html')


bot.polling()