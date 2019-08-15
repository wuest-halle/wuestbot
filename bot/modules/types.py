"""
provides the necessary data types, for now only the bot() type
"""

import json
import requests
import os
import pathlib

import dotenv # temporary to use .env file - to be removed when this becomes a flask app

class Telebot:

    def __init__(self, API_TOKEN):

        self.API_TOKEN = API_TOKEN
        self.URL = f"https://api.telegram.org/bot{API_TOKEN}/"

    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf-8")
        return content
    
    def parse_json(self, url):
        content = self.get_url(url)
        content = json.loads(content)
        for item in content:
            print (item)
    
    def get_updates(self, offset=None):
        url = self.URL + "getUpdates"
        if offset:
            url += f"?offset={offset}"
        self.parse_json(url)