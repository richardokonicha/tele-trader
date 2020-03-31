
# import os
# from flask import Flask, request
# from config import *
# import handlers

# # TOKEN = "746406709:AAHGsGOKxHwPOhRMdUOM5JNKsVxI2cCTbyQ"
# TOKEN = "852053528:AAHL_ryUUJ1JOhenzmI0WDiayAnxxqGFmyU"
# bot = telebot.TeleBot(TOKEN)
# server = Flask(__name__)


# # @server.route('/' + TOKEN, methods=['POST'])
# # def getMessage():
# #     bot.process_new_updates(
# #         [telebot.types.Update.de_json(
# #             request.stream.read().decode("utf-8")
# #             )])
# #     return "!getmessage", 200




# @server.route('/'+ TOKEN, methods=['POST'])
# def getMessage():
#     request_object = request.stream.read().decode("utf-8")
#     update_to_json = [telebot.types.Update.de_json(request_object)]
#     bot.process_new_updates(update_to_json)
#     return "got Message bro"

# @server.route("/")
# def webhook():
#     url='https://fcx-bot.herokuapp.com/'
#     url="https://6d92275c.ngrok.io/"
#     bot.remove_webhook()
#     bot.set_webhook(url + TOKEN)
#     return "!webhook is set", 200


# if __name__ == "__main__":
#     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


from flask import Flask, request
import os
import handlers
from config import *

server = Flask(__name__)


@server.route('/'+ TOKEN, methods=['POST'])
def getMessage():
    request_object = request.stream.read().decode("utf-8")
    update_to_json = [telebot.types.Update.de_json(request_object)]
    bot.process_new_updates(update_to_json)
    return "got Message bro"


@server.route('/')
def webhook():
    # url="https://6d92275c.ngrok.io/"
    url='https://fcx-bot.herokuapp.com/'
    bot.remove_webhook()
    bot.set_webhook(url + TOKEN)
    return f"Webhook set to {url}mytoken"

# handlers.bot.polling()

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))