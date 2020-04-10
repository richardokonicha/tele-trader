
from config import *

@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and (
        bool(re.search(r'Transactions', message.text, re.IGNORECASE))
         or  bool(re.search(r'Transazioni$', message.text, re.IGNORECASE))
        )
)
def transaction(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    fcx_user = db.User.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language
    transactions = db.Transactions.get_transactions(user_id)
    deposits = []
    payouts = []
    reinvestments = []
    commissions = []
    for value in transactions:
        if value.transaction_type=="deposit":
            deposits.append(value.date.split("T")[0]+"  "+str(value.amount))
        if value.transaction_type=="withdrawal":
            payouts.append(value.date.split("T")[0]+"  "+str(value.amount))
        if value.transaction_type=="reinvestment":
            reinvestments.append(value.date.split("T")[0]+"  "+str(value.amount))
        if value.transaction_type=="commissions":
            commissions.append(value.date.split("T")[0]+"  "+str(value.amount))

    text_info = {
        "en": f"""

Deposits:
.....
30/03/2020 0.022111 BTC 
23/03/2020 0.500000 BTC   
{deposits}


Payouts:
.....
30/04/2020 0.022111 BTC 
27/03/2020 0.500000 BTC


Reinvestments:
......
15/07/2020 0.500000 BTC
15/06/2020 0.022111 BTC

Commissions:
.....
17/08/2020 0.500000 BTC
08/06/2020 0.022111 BTC

        """,
        "it": f"""
Depositi:
.....
30/03/2020 0,022111 BTC   
23/03/2020 0.500000 BTC 

Pagamenti:
.....
30/04/2020 0,022111 BTC
27/03/2020 0.500000 BTC

Reinvestimenti:
......
15/07/2020 0,500000 BTC
15/06/2020 0,022111 BTC

Commissioni:
.....
17/08/2020 0,500000 BTC
08/06/2020 0.022111 BTC 


        """
        }


    bot.send_message(
        chat_id, text=text_info[lang],
        reply_markup=dashboard.get(lang), parse_mode="html"
        )

