from flask import Flask, request, render_template, flash
import os
from config import *
from settings import URL
from database.forms import AdminForm
server = Flask(__name__)


def split_filter(n):
    return n.split("T")[0]
server.jinja_env.filters["splitfilter"] = split_filter

def count_filter(n):
    return len(n)
server.jinja_env.filters["countfilter"] = count_filter

def moneysum(n):
    amounts = Decimal()
    for transac in n:
        amounts = amounts + transac.amount
    return amounts
server.jinja_env.filters["moneysum"] = moneysum

def dashUpdate(form, admin_db):
    admin_db.user_id = form['admin_userid']
    admin_db.merchant_ID = form['merchant_ID']
    admin_db.merchant_pbkey = form['merchant_pbkey']
    admin_db.merchant_pkey = form['merchant_pkey']
    admin_db.daily_profits = form['daily_profits']
    admin_db.duration_reinvest = form['duration_reinvest']

    admin_db.commit()
    return admin_db

##############################

@server.route('/'+ TOKEN, methods=['POST'])
def getMessage():
    request_object = request.stream.read().decode("utf-8")
    update_to_json = [telebot.types.Update.de_json(request_object)]
    bot.process_new_updates(update_to_json)
    return "got Message bro"

# @server.route("/")
# def pay():
#     return "This is the fcx trading bot you can reach me @FCX_trading_bot on telegram"

@server.route('/dashboard')
def dashboard():
    request_web = request
    admin_db = db.session.query(db.Admin).first()
    all_users = db.session.query(db.User).all()
    deposit = db.session.query(db.Transactions).filter(db.Transactions.transaction_type=="deposit").all()
    withdrawal = db.session.query(db.Transactions).filter(db.Transactions.transaction_type=="withdrawal").all()
    investment = db.session.query(db.Transactions).filter(db.Transactions.transaction_type=="investments").all()
    form = {
        "users": all_users,
        "deposit": deposit,
        "withdrawal": withdrawal,
        "investment": investment
    }
    return render_template('admin_dashboard/dist/index.html', form=form)

@server.route('/settings', methods=["POST", "GET"])
def settings():
    request_web = request
    admin_db = db.session.query(db.Admin).first()
    form = request_web.form
    if request_web.method == 'POST':
        admin = dashUpdate(form, admin_db)
        return render_template('admin_dashboard/dist/settings.html', form=admin_db)
    return render_template('admin_dashboard/dist/settings.html', form=admin_db)

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
            fcx_dp.recieved_amount = Decimal(value.get('received_amount'))
            fcx_dp.dp_status_text = value["status_text"]
            status = value['status']
            fcx_dp.status = status
            fcx_dp.commit()
            text=f"""
Created Transaction
Transaction ID: <b>{txn_id}</b>
Address: <b>{fcx_dp.dp_address}</b>
Amount : <b>{value['amount1']}</b>
Says: <b>{fcx_dp.dp_status_text}</b>
            """
            bot.send_message(
                fcx_dp.user.user_id,
                text=text,
                reply_markup=dashboard[fcx_dp.user.language],
                parse_mode="html"
            )
            if status=='100':
                fcx_dp.user.account_balance = fcx_dp.user.account_balance + fcx_dp.recieved_amount
                fcx_dp.commit()
                text = f"You have been credited {fcx_dp.recieved_amount}"
                dashboard['lang'].keyboard[0][0] = f"Balances  {fcx_user.account_balance} BTC"
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