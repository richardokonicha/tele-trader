
import os
from flask import Flask, request
from config import *
import handlers

TOKEN = "746406709:AAHGsGOKxHwPOhRMdUOM5JNKsVxI2cCTbyQ"
# TOKEN = "852053528:AAHL_ryUUJ1JOhenzmI0WDiayAnxxqGFmyU"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(
            request.stream.read().decode("utf-8")
            )])
    return "!getmessage", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://fcx-bot.herokuapp.com/' + TOKEN)
    return "!webhook", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
