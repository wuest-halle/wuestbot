#!/usr/bin/env python

""" TO DO:
- proper error management if python can't parse token (applies to all html code)
- save known chat ids in file, so they dont have to restart every time
"""

import os

from dotenv import load_dotenv
import telebot

# load env variables from .env
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

template_dir = os.path.abspath('../bot/templates')
img_dir = os.path.abspath('../bot/img')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['test'])
def test(message):
	with open(os.path.join(template_dir, 'test.html'), 'r') as f:
		reply = f.read()
	bot.send_message(chat_id=message.chat.id, text=reply, parse_mode='html')

# returns flyer and info on the next event when user sends /next
@bot.message_handler(commands=['next'])
def next_event(message):
	with open(os.path.join(template_dir,  'next_event.html'), 'r') as f:
		photo_caption = f.read()
	with open(os.path.join(img_dir, 'next_event.jpg'), 'rb') as p:
		picture=p.read()
	bot.send_photo(chat_id=message.chat.id, photo=picture, caption=photo_caption, parse_mode='html')


bot.polling()