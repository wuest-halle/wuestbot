#!/usr/bin/env python
# coding=utf8

""" This is the main application module with all the logic in it """

import time
import json
import dotenv
import os

from modules import types
from app import app

"""
loads all environment vars from the .env file and makes them available
"""
class Config:
    dotenv.load_dotenv()

    API_TOKEN = os.getenv("API_TOKEN")


def main():
    bot = types.Telebot(Config.API_TOKEN)
    bot.get_updates()


if __name__ == "__main__":
    main()