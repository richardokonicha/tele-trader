
from config import *

@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and ( 
        bool(re.search(r'^Transactions$', message.text, re.IGNORECASE))
         or  bool(re.search(r'^Transazioni$', message.text, re.IGNORECASE))
        )
)
def transaction(message):
    chat_id = message.chat.id
    user_object = get_user(message)
    balance = user_object["investment"]['balance']
    lang = user_object["lang"]
    text_info = {
        "ENGLISH": f"""

Deposits:
.....
30/03/2020 0.022111 BTC 
23/03/2020 0.500000 BTC     


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
        "ITALIAN": f"""
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

