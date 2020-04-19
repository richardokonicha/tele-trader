import json
import re
import telebot
from telebot import types
from functions import *
from coinpayment import CoinPayments
from datetime import datetime
from database import database as db
from settings import PRIVATE_KEY, PUBLIC_KEY, ADMIN_ID
from settings import TOKEN
# from settings import TOKEN_TEST as TOKEN


# bot = telebot.TeleBot(TOKEN, threaded=True)
bot = telebot.TeleBot(TOKEN, threaded=True)

payment_client = CoinPayments(PUBLIC_KEY, PRIVATE_KEY, ipn_url="https://a307ef5b.ngrok.io/pay")


######### keyboard markup below here #######

from telebot import types
keys = types.ReplyKeyboardMarkup()


force_r = types.ForceReply()

select_lang_markup = [
    ["English  🇬🇧", "Italiano  🇮🇹"]
]


fcx_markup = {

"en": [
    ["Balance BTC"],
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

# fcx_markup_balances = {
#     "en": f"Balances  {fcx_user.account_balance} BTC",
#     "it": f"Bilance  {fcx_user.account_balance} BTC"
# }


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





################# ADDRESS 
en_confirm_markup = types.InlineKeyboardMarkup(row_width=2)
it_confirm_markup = types.InlineKeyboardMarkup()

en_confirm_btn = types.InlineKeyboardButton(text="Confirm", callback_data="confirm_address")
en_modify_btn = types.InlineKeyboardButton(text="Cancel", callback_data="cancel_address")

it_confirm_btn = types.InlineKeyboardButton(text="Confermare", callback_data="confirm_address")
it_modify_btn = types.InlineKeyboardButton(text="Annulla", callback_data="cancel_address")

# en_confirm_markup.keyboard = [[en_confirm_btn], [en_modify_btn]]
# it_confirm_markup.keyboard = [[it_confirm_btn], [it_modify_btn]]

en_confirm_markup.add(en_confirm_btn, en_modify_btn)
it_confirm_markup.add(it_confirm_btn, it_modify_btn)


confirm = {
    "en": en_confirm_markup,
    "it": it_confirm_markup
}


################ ADDRESS ENDS


################ ORDER #########

en_confirm_order_markup = types.InlineKeyboardMarkup(row_width=2)
it_confirm_order_markup = types.InlineKeyboardMarkup()

en_confirm_order_btn = types.InlineKeyboardButton(text="Confirm", callback_data="confirm_order")
it_confirm_order_btn = types.InlineKeyboardButton(text="Confermare", callback_data="confirm_order")

en_cancel_order_btn = types.InlineKeyboardButton(text="Cancel", callback_data="cancel_order")
it_cancel_order_btn = types.InlineKeyboardButton(text="Annulla", callback_data="cancel_order")
# en_confirm_markup.keyboard = [[en_confirm_btn], [en_modify_btn]]
# it_confirm_markup.keyboard = [[it_confirm_btn], [it_modify_btn]]
en_confirm_order_markup.add(en_confirm_order_btn, en_cancel_order_btn)
it_confirm_order_markup.add(it_confirm_order_btn, it_cancel_order_btn)
confirm_order = {
    "en": en_confirm_order_markup,
    "it": it_confirm_order_markup
}
##################


############################reinvestment


en_confirm_reinvestment_markup = types.InlineKeyboardMarkup(row_width=2)
it_confirm_reinvestment_markup = types.InlineKeyboardMarkup(row_width=2)

en_confirm_reinvestment_btn = types.InlineKeyboardButton(text="Confirm", callback_data="confirm_reinvestment")
it_confirm_reinvestment_btn = types.InlineKeyboardButton(text="Confermare", callback_data="confirm_reinvestment")

en_cancel_reinvestment_btn = types.InlineKeyboardButton(text="Cancel", callback_data="cancel_reinvestment")
it_cancel_reinvestment_btn = types.InlineKeyboardButton(text="Annulla", callback_data="cancel_reinvestment")

en_confirm_reinvestment_markup.add(en_confirm_reinvestment_btn, en_cancel_reinvestment_btn)
it_confirm_reinvestment_markup.add(it_confirm_reinvestment_btn, it_cancel_reinvestment_btn)
confirm_reinvestment = {
    "en": en_confirm_reinvestment_markup,
    "it": it_confirm_reinvestment_markup
}

#############################reinvestment



########## keyboard layout defination ends #


withdrawal_minimum_amount = 0.002

import importdir
importdir.do("features", globals())
