import json
import re
import telebot
from telebot import types
from functions import *
from coinpayment import CoinPayments
from datetime import datetime

from database import database as db

from settings import PRIVATE_KEY, PUBLIC_KEY, ADMIN_ID, TEST_URL, PROD_URL
from settings import TOKEN_PRODUCTION as TOKEN

# bot = telebot.TeleBot(TOKEN, threaded=True)
bot = telebot.TeleBot(TOKEN, threaded=True)

payment_client = CoinPayments(PUBLIC_KEY, PRIVATE_KEY)


######### keyboard markup below here #######

from telebot import types
keys = types.ReplyKeyboardMarkup()


force_r = types.ForceReply()

select_lang_markup = [
    ["English  🇬🇧", "Italian  🇮🇹"]
]


fcx_markup = {

"en": [
    ["Balances BTC"],
    ["🏦 Deposit", "🏧 Withdrawal"],
    ["💵 Reinvest", "📜 Transactions"],
    ["⛳ Team", "🇬🇧 Language", "🤝 Support"]
    ],
    
"it": [
    ["Bilance BTC"],
    ["🏦 Depositare", "🏧 Ritiro"],
    ["💵 Reinvest", "📜 Transazioni"],
    ["⛳ Squadra", "🇬🇧 linguaggio", "🤝 Supporto"]
    ]
}



######### keyboard markup above here #######

########## keyboard layout defination ######3
en_home_keys = types.ReplyKeyboardMarkup()
it_home_keys = types.ReplyKeyboardMarkup()
en_home_keys.keyboard = fcx_markup.get("en")
it_home_keys.keyboard = fcx_markup.get("it")


dashboard = {
    "en": en_home_keys,
    "it": it_home_keys
}

lang_keys = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
    )
lang_keys.keyboard = select_lang_markup
########## keyboard layout defination ends #

import importdir
importdir.do("features", globals())
