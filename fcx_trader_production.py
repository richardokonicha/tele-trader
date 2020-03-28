
import os

from flask import Flask, request
import telebot
from telebot import types
from core import fcx_markup, welcome_text


TOKEN = "746406709:AAHGsGOKxHwPOhRMdUOM5JNKsVxI2cCTbyQ"
# TOKEN = "852053528:AAHL_ryUUJ1JOhenzmI0WDiayAnxxqGFmyU"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

keys = types.ReplyKeyboardMarkup()


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        text=welcome_text,
        reply_markup=keys,
        parse_mode="HTML"
        )




@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text, "coming soon")


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!getmessage", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://fcx-bot.herokuapp.com/' + TOKEN)
    return "!webhook", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
