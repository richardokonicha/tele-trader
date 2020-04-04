from config import *

@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and ( 
        bool(re.search(r'Reinvest$', message.text, re.IGNORECASE))
        #  or  bool(re.search(r'^Ritiro$', message.text.split()[1], re.IGNORECASE))
        )
)
def reinvest(message):
    chat_id = message.chat.id
    user_object = get_user(message)
    balance = user_object["investment"]['balance']
    lang = user_object["lang"]
    withdrawal_minimum_amount = 0.002
    text_info = {
        "ENGLISH": f"""
You can make a reinvest any time, depending on your account balance . 
Minimum amount to reinvest is 0.002 BTC. Once credited, each reinvestment counts for itself and runs for 180 days.
        """,
        "ITALIAN": f"""
Potete effettuare un reinvestimento in qualsiasi momento, a seconda del saldo del Vostro conto. L'importo minimo da reinvestire è di 0,002 BTC. Una volta accreditato, ogni reinvestimento vale per se stesso e dura 180 giorni.
        """
        }
    text_insufficient = {
        "ENGLISH": """
You don't have enough funds to create a reinvest
        """,
        "ITALIAN": """
Non avete abbastanza fondi per creare un reinvestimento. 
        """
    }
    text_enter_amount = {
        "ENGLISH": """
Please enter the amount to reinvest:
        """,
        "ITALIAN": """
Per favore inserire l'importo da reinvestire:
        """
    }
    if balance < withdrawal_minimum_amount:
        bot.send_message(
            chat_id, text=text_info[lang] + text_insufficient[lang],
            reply_markup=home_keys, parse_mode="html"
            )
    else:
        bot.send_message(
            chat_id, text=text_info[lang] + text_enter_amount[lang],
            reply_markup=dashboard.get(lang), parse_mode="html"
            )

