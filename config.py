import importdir
import json
import re
import telebot
from telebot import types
from functions import *
from coinpayment import CoinPayments
from datetime import datetime
from decimal import *
from database import database as db
from settings import TOKEN, URL

bot = telebot.TeleBot(TOKEN, threaded=True)
admin_db = db.session.query(db.Admin).first()

MERCHANT_ID = admin_db.merchant_ID
PUBLIC_KEY = admin_db.merchant_pbkey
PRIVATE_KEY = admin_db.merchant_pkey
ADMIN_ID = admin_db.user_id
payment_client = CoinPayments(PUBLIC_KEY, PRIVATE_KEY, ipn_url=URL + "pay")

keys = types.ReplyKeyboardMarkup()
force_r = types.ForceReply()
en_home_keys = types.ReplyKeyboardMarkup()
it_home_keys = types.ReplyKeyboardMarkup()

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
dashboard = {
    "en": en_home_keys,
    "it": it_home_keys
}
en_home_keys.keyboard = fcx_markup.get("en")
it_home_keys.keyboard = fcx_markup.get("it")

lang_keys = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
)
lang_keys.keyboard = select_lang_markup

en_confirm_markup = types.InlineKeyboardMarkup(row_width=2)
it_confirm_markup = types.InlineKeyboardMarkup()

en_confirm_btn = types.InlineKeyboardButton(
    text="Confirm", callback_data="confirm_address")
en_modify_btn = types.InlineKeyboardButton(
    text="Cancel", callback_data="cancel_address")

it_confirm_btn = types.InlineKeyboardButton(
    text="Confermare", callback_data="confirm_address")
it_modify_btn = types.InlineKeyboardButton(
    text="Annulla", callback_data="cancel_address")

en_confirm_markup.add(en_confirm_btn, en_modify_btn)
it_confirm_markup.add(it_confirm_btn, it_modify_btn)

confirm = {
    "en": en_confirm_markup,
    "it": it_confirm_markup
}

en_confirm_order_markup = types.InlineKeyboardMarkup(row_width=2)
it_confirm_order_markup = types.InlineKeyboardMarkup()

en_confirm_order_btn = types.InlineKeyboardButton(
    text="Confirm", callback_data="confirm_order")
it_confirm_order_btn = types.InlineKeyboardButton(
    text="Confermare", callback_data="confirm_order")

en_cancel_order_btn = types.InlineKeyboardButton(
    text="Cancel", callback_data="cancel_order")
it_cancel_order_btn = types.InlineKeyboardButton(
    text="Annulla", callback_data="cancel_order")
en_confirm_order_markup.add(en_confirm_order_btn, en_cancel_order_btn)
it_confirm_order_markup.add(it_confirm_order_btn, it_cancel_order_btn)
confirm_order = {
    "en": en_confirm_order_markup,
    "it": it_confirm_order_markup
}

en_confirm_reinvestment_markup = types.InlineKeyboardMarkup(row_width=2)
it_confirm_reinvestment_markup = types.InlineKeyboardMarkup(row_width=2)

en_confirm_reinvestment_btn = types.InlineKeyboardButton(
    text="Confirm", callback_data="confirm_reinvestment")
it_confirm_reinvestment_btn = types.InlineKeyboardButton(
    text="Confermare", callback_data="confirm_reinvestment")

en_cancel_reinvestment_btn = types.InlineKeyboardButton(
    text="Cancel", callback_data="cancel_reinvestment")
it_cancel_reinvestment_btn = types.InlineKeyboardButton(
    text="Annulla", callback_data="cancel_reinvestment")

en_confirm_reinvestment_markup.add(
    en_confirm_reinvestment_btn, en_cancel_reinvestment_btn)
it_confirm_reinvestment_markup.add(
    it_confirm_reinvestment_btn, it_cancel_reinvestment_btn)
confirm_reinvestment = {
    "en": en_confirm_reinvestment_markup,
    "it": it_confirm_reinvestment_markup
}

withdrawal_minimum_amount = 0.002
importdir.do("features", globals())
