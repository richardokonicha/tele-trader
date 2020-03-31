import json
import re

import telebot
from telebot import types

from functions import database, first_name, get_add_user, get_user, set_lang



# TOKEN = "852053528:AAHL_ryUUJ1JOhenzmI0WDiayAnxxqGFmyU"
TOKEN = "746406709:AAHGsGOKxHwPOhRMdUOM5JNKsVxI2cCTbyQ"


bot = telebot.TeleBot(TOKEN)



######### keyboard markup below here #######

from telebot import types
keys = types.ReplyKeyboardMarkup()


select_lang_markup = [
    ["ENGLISH", "ITALIAN"]
]

fcx_markup = [
    ["Balances BTC"],
    ["Deposit", "Withdrawal"],
    ["Reinvest", "Transactions"],
    ["Team", "Language", "Support"]
    ]
######### keyboard markup above here #######

########## keyboard layout defination ######3
home_keys = types.ReplyKeyboardMarkup()
home_keys.keyboard = fcx_markup


lang_keys = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
    )
lang_keys.keyboard = select_lang_markup
########## keyboard layout defination ends #

