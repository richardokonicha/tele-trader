import json
from email import message

import telebot
from setuptools import command
from telebot import types

from core import *
from core import select_lang_markup
from functions import database, first_name, get_add_user, get_user, set_lang

TOKEN = "852053528:AAHL_ryUUJ1JOhenzmI0WDiayAnxxqGFmyU"

bot = telebot.TeleBot(TOKEN)

home_keys = types.ReplyKeyboardMarkup()
home_keys.keyboard = fcx_markup



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
            text=responses["select_prefered_lang"],
            reply_markup=lang_keys,
            parse_mode="HTML"
            )
    else:
        bot.send_message(
            chat_id,
            text=responses["welcome_text"][user_object["lang"]],
            reply_markup=home_keys,
            parse_mode="HTML"
            )


@bot.message_handler(commands=["language"])
def show_language(message):
    chat_id = message.chat.id

    bot.send_message(
            chat_id,
            text=responses["select_prefered_lang"],
            reply_markup=lang_keys,
            parse_mode="HTML"
            )


@bot.message_handler(
    func=lambda message: message.content_type == 'text' and 
    message.text in ['ENGLISH', 'ITALIAN']
    )
def set_langauge(message):
    """sets language and returns language value and send user confirmation message"""
    chat_id = message.chat.id
    user_object = get_user(message)
    language = set_lang(user_object["user_id"], message.text)
    text=responses["set_lang_text"][language],
    bot.send_message(
        chat_id,
        text=text,
        reply_markup=home_keys
    )

bot.polling()
