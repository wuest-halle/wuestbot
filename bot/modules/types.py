"""
provides the necessary data types, for now only the bot() type
"""

import json
import requests

class Telebot:

    def __init__(self, API_TOKEN):
        self.API_TOKEN = API_TOKEN
        self.URL = f"https://api.telegram.org/bot{API_TOKEN}/"
        self.last_update=""

    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf-8")
        return content
    
    def parse_json(self, url):
        content = self.get_url(url)
        content = json.loads(content)
        for item in content["result"]:              # these are just primitive debug prints, gonna be removed
            print (item["message"]["text"])
        last_id = len(content["result"]) - 1
        if content["result"][last_id]["update_id"] != self.last_update:
            self.last_update = content["result"][last_id]["update_id"]
    
    def get_updates(self):
        url = self.URL + "getUpdates"
        if self.last_update:
            url += f"?offset={int(self.last_update) + 1}"
        self.parse_json(url)