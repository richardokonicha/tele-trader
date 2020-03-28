import telebot
from telebot import types
from core import fcx_markup, welcome_text

TOKEN = "852053528:AAHL_ryUUJ1JOhenzmI0WDiayAnxxqGFmyU"

bot = telebot.TeleBot(TOKEN)

keys = types.ReplyKeyboardMarkup()
# keys = types.InlineKeyboardMarkup()
keys.keyboard = fcx_markup


@bot.message_handler(commands=["start"])
def menu(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        text=welcome_text,
        reply_markup=keys,
        parse_mode="HTML"
        )

bot.polling()


