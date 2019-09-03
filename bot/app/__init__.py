from os import getenv

from flask import Flask, request
from telebot import TeleBot
from dotenv import load_dotenv

load_dotenv()

global token
global url
token = getenv('API_TOKEN')
url = getenv('URL')
bot = TeleBot(token)
app = Flask(__name__)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)

@app.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([bot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route('/set_webhook', methods=['GET', 'POST'])
def webhook():
    bot.remove_webhook()
    hook = bot.set_webhook(f'{url}{token}')
    if hook:
        return "webhook setup okay", 200
    else:
        return "webhook setup failed", 404


if __name__ == "__main__":
    app.run(threaded=True)
