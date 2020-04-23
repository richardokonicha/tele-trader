from flask import Flask, request
import os
from config import *
from settings import URL


server = Flask(__name__)


@server.route('/'+ TOKEN, methods=['POST'])
def getMessage():
    request_object = request.stream.read().decode("utf-8")
    update_to_json = [telebot.types.Update.de_json(request_object)]
    bot.process_new_updates(update_to_json)
    return "got Message bro"



# @server.route("/")
# def pay():
#     return "This is the fcx trading bot you can reach me @FCX_trading_bot on telegram"

@server.route('/hook')
def webhook():
    url=URL
    bot.remove_webhook()
    bot.set_webhook(url + TOKEN)
    return f"Webhook set to {url}"

@server.route('/pay', methods=['POST'])
def index():
    url=URL
    requests=request
    try:
        
        value = requests.values
        txn_id = value["txn_id"]
        fcx_dp = db.Transactions.get_txn_id(txn_id)
        if fcx_dp != None:
            fcx_dp.status_text = value["status_text"]
            fcx_dp.status = value["status"]
            fcx_dp.commit()
            text=f"""
Created Transaction
Transaction ID: <b>{txn_id}</b>
Amount : <b>{value['amount1']}</b>
Says: <b>{value['status_text']}</b>
            
            """
            bot.send_message(
                fcx_dp.user.user_id,
                text=text,
                reply_markup=dashboard[fcx_dp.user.language],
                parse_mode="html"
            )
        else:
            pass
    except KeyError:
        pass

    print(request)
    return f"To set webhook goto to <a href='{url}hook'>{url}hook</a>"


# @server.route('/pay', methods=['GET'])
# def index():
#     url=URL
#     return f"To set webhook goto to <a href='{url}hook'>{url}hook</a>"

# bot.remove_webhook()
# bot.polling()

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))