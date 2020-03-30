import json
import re

import telebot
from telebot import types

from core import *
from core import select_lang_markup, fcx_markup
from functions import database, first_name, get_add_user, get_user, set_lang



TOKEN = "852053528:AAHL_ryUUJ1JOhenzmI0WDiayAnxxqGFmyU"

bot = telebot.TeleBot(TOKEN)

home_keys = types.ReplyKeyboardMarkup()
home_keys.keyboard = fcx_markup


lang_keys = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
    )
lang_keys.keyboard = select_lang_markup

