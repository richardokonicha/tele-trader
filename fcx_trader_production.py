
from flask import Flask, request
import os
# import handlers
from config import *


server = Flask(__name__)


@server.route('/'+ TOKEN, methods=['POST'])
def getMessage():
    request_object = request.stream.read().decode("utf-8")
    update_to_json = [telebot.types.Update.de_json(request_object)]
    bot.process_new_updates(update_to_json)
    return "got Message bro"



@server.route("/pay", methods=["POST"])
def pay():
    requests = request
    return requests

@server.route('/')
def webhook():
    url=PROD_URL
    bot.remove_webhook()
    bot.set_webhook(url + TOKEN)
    return f"Webhook set to {url}"

# handlers.bot.polling()

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))