import json
import re
import telebot
from telebot import types
from functions import *
from coinpayment import CoinPayments
from datetime import datetime

TOKEN = "852053528:AAHL_ryUUJ1JOhenzmI0WDiayAnxxqGFmyU"
# TOKEN = "746406709:AAHGsGOKxHwPOhRMdUOM5JNKsVxI2cCTbyQ" #fcxtrader bot
# TOKEN = "1137661512:AAEig943WBK2aCBhlrDxgpN6Tl__lpxOMUY" #FCX trading bot


# # Key Name: Unnamed API Key
PublicKey = "953b0c668c9d75c2d3da984f62a00fd269dc66c6da701250a0d7e14b52449183"
PrivateKey = "c68f21F77B13FE4D6617EfcD0287c036da7A3aB1A5f3e870fb179E940F5839Dd"
ipn_url="https://0218d890.ngrok.io/pay"



# bot = telebot.TeleBot(TOKEN, threaded=True)
bot = telebot.AsyncTeleBot(TOKEN, threaded=True)

payment_client = CoinPayments(PublicKey, PrivateKey)


######### keyboard markup below here #######

from telebot import types
keys = types.ReplyKeyboardMarkup()


force_r = types.ForceReply()

select_lang_markup = [
    ["English  🇬🇧", "Italian  🇮🇹"]
]


fcx_markup = {

"ENGLISH": [
    ["Balances BTC"],
    ["🏦 Deposit", "🏧 Withdrawal"],
    ["💵 Reinvest", "📜 Transactions"],
    ["⛳ Team", "🇬🇧 Language", "🤝 Support"]
    ],
    
"ITALIAN": [
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
en_home_keys.keyboard = fcx_markup.get("ENGLISH")
it_home_keys.keyboard = fcx_markup.get("ITALIAN")


dashboard = {
    "ENGLISH": en_home_keys,
    "ITALIAN": it_home_keys
}

lang_keys = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
    )
lang_keys.keyboard = select_lang_markup
########## keyboard layout defination ends #

import importdir
importdir.do("features", globals())
