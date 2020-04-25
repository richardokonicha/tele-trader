from config import *


# @bot.callback_query_handler(func=lambda call: True)
# def callback_answer(call):
#         user_id = call.from_user.id
#         fcx_user = db.User.get_user(user_id)
#         balance = fcx_user.account_balance
#         lang = fcx_user.language
#         if call.data == "confirm_reinvestment":
#                 pass




# called when reinvest is replied

def process_reinvest(message):
        pass


def verify_reinvest(message):
        user_id = message.from_user.id
        fcx_user = db.User.get_user(user_id)
        chat_id = message.chat.id
        # fcx_user = db.User.get_user(user_id)
        reply_from = message.reply_to_message.text
        if reply_from in ["Please enter the amount to reinvest:", "Per favore inserire l'importo da reinvestire:"]:
                balance = fcx_user.account_balance
                lang = fcx_user.language
                fcx_markup_balances = {
                        "en": f"Balances  {fcx_user.account_balance} BTC",
                        "it": f"Bilance  {fcx_user.account_balance} BTC"
                        }
                dashboard[lang].keyboard[0][0] = fcx_markup_balances[lang]
                try:
                        reinvestment_amount = Decimal(message.text)
                        if reinvestment_amount > balance:
                                text_insufficient = {
                                        "en": "You have insufficient account balance",
                                        "it": "Hai un saldo del conto insufficiente"
                                }
                                bot.reply_to(
                                        message,
                                        text=text_insufficient[lang],
                                        reply_markup=dashboard[lang]
                                )
                        elif reinvestment_amount < 0:
                                invalid_amount = {
                                        "en": "Invalid reinvestment amount",
                                        "it": "Importo del reinvestimento non valido"
                                        }
                                bot.reply_to(
                                        message,
                                        text=invalid_amount[lang],
                                        reply_markup=dashboard[lang]
                                        )
                        else:
                                investment_confirmation = {
                                        "en": f"""
        You're about to make a reinvestment of:{reinvestment_amount} BTC""",
                                        "it": f"""
        Stai per effettuare un reinvestimento di:{reinvestment_amount} BTC"""
                                }
                                bot.send_message(
                                        chat_id,
                                        text=investment_confirmation[lang],
                                        reply_markup=confirm_reinvestment[lang]
                                )
                except ValueError as err:
                        invalid_amount = {
                                "en": "Invalid reinvestment amount",
                                "it": "Invalid reinvestment amount (italian)"
                                }
                        bot.reply_to(
                                message, 
                                text=invalid_amount[lang],
                                reply_markup=dashboard[lang]
                        )


@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and ( 
        bool(re.search(r'Reinvest$', message.text, re.IGNORECASE))
        #  or  bool(re.search(r'^Ritiro$', message.text.split()[1], re.IGNORECASE))
        )
)
def reinvest(message):
        
        user_id = message.from_user.id
        chat_id = message.chat.id
        fcx_user = db.User.get_user(user_id)
        balance = fcx_user.account_balance
        lang = fcx_user.language

        fcx_markup_balances = {
        "en": f"Balances  {fcx_user.account_balance} BTC",
        "it": f"Bilance  {fcx_user.account_balance} BTC"
        }
        dashboard[lang].keyboard[0][0] = fcx_markup_balances[lang]
        text_info = {
                "en": f"""
You can make a reinvest any time, depending on your account balance . 
Minimum amount to reinvest is 0.002 BTC. Once credited, each reinvestment counts for itself and runs for 180 days.
        """,
                "it": f"""
Potete effettuare un reinvestimento in qualsiasi momento, a seconda del saldo del Vostro conto. L'importo minimo da reinvestire è di 0,002 BTC. Una volta accreditato, ogni reinvestimento vale per se stesso e dura 180 giorni.
        """
        }
        text_insufficient = {
                "en": """
You don't have enough funds to create a reinvest
        """,
                "it": """
Non avete abbastanza fondi per creare un reinvestimento. 
        """
    }
        text_enter_amount = {
                "en": """
<b>Please enter the amount to reinvest:</b>
        """,
                "it": """
<b>Per favore inserire l'importo da reinvestire:</b>
        """
    }
        if balance < withdrawal_minimum_amount:
                bot.send_message(
                chat_id, text=text_info[lang] + text_insufficient[lang],
                reply_markup=dashboard[lang], parse_mode="html"
                )
        else:

                bot.send_message(
                        chat_id,
                        text=text_info[lang]
                )
                bot.send_message(
                        chat_id, 
                        text=text_enter_amount[lang],
                        # reply_markup=dashboard.get(lang),
                        parse_mode="html",
                        reply_markup=force_r
                )
                bot.register_next_step_handler(message, verify_reinvest)
               
