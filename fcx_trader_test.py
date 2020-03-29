import json

import telebot
from telebot import types

from core import *
from core import select_lang_markup
from functions import database, first_name, lang, get_add_user

TOKEN = "852053528:AAHL_ryUUJ1JOhenzmI0WDiayAnxxqGFmyU"

bot = telebot.TeleBot(TOKEN)

keys = types.ReplyKeyboardMarkup()
keys.keyboard = fcx_markup



lang_keys = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
lang_keys.keyboard = select_lang_markup



@bot.message_handler(commands=["start"])
def start(message):
    """this is the starting point, it checks if user is not registered 
    and renders lang settings if user is registered uses pervious lang """
    chat_id = message.chat.id
    user_object = get_add_user(message)
    
    if user_object["is_new_user"] == True:
        bot.send_message(
            chat_id,
            text=select_lang_text,
            reply_markup=lang_keys,
            parse_mode="HTML"
            )
    else:
        bot.send_message(
            chat_id,
            text=welcome_text,
            reply_markup=keys,
            parse_mode="HTML"
            )


@bot.message_handler(commands=["ENGLISH"])
def menu_english(message):
    chat_id = message.chat.id

    bot.send_message(
        chat_id,
        text=welcome_text,
        reply_markup=keys,
        parse_mode="HTML"
        )

bot.polling()
