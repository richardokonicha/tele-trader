from config import *



def wallet_amount_confirmation(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    message_id = message.message_id + 1
    fcx_user = db.User.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language
    amount = message.text
    try:
        amount = Decimal(amount)
        if amount > balance:
            insufficient_balance_text = {
                "en": "You don't have enough funds to create a payout request",
                "it": "Non puoi prelevare un valore superiore al saldo del tuo account"
            }
            bot.send_message(
                chat_id, 
                text=insufficient_balance_text[lang], 
                parse_mode="html",
                reply_markup=force_r
                )
            bot.register_for_reply_by_message_id(
                message_id, 
                wallet_amount_confirmation
            )
            # bot.register_next_step_handler(
            #     message, 
            #     wallet_amount_confirmation
            #     )
        else:
            try:
                set_wallet_address_text = {
                    'en': "<b>Set your BTC wallet address</b>",
                    'it': "<b>Imposta l'indirizzo del tuo portafoglio BTC</b>"
                }
                bot.send_message(
                    chat_id, 
                    text=set_wallet_address_text[lang], 
                    parse_mode="html",
                    reply_markup=force_r
                    )
                bot.register_for_reply_by_message_id(
                    message_id,
                    wallet_address_confirmation,
                    (amount)
                )
                    # set_wallet_address(message)  
            except KeyError:
                bot.send_message(chat_id, text="Invalid wallet address", parse_mode="html")
                set_wallet_address(message)
    except (ValueError, InvalidOperation) as e:
        invalid_amount = {
            "en": "Invalid amount please insert number",
            "it": "Importo non valido inserire il numero"

        }
        bot.send_message(
            chat_id, 
            text=invalid_amount[lang], 
            parse_mode="html",
            reply_to_message_id=message.message_id
            )
        bot.register_next_step_handler(
            message, 
            wallet_amount_confirmation
            )


def wallet_address_confirmation(message, amount):
    chat_id = message.chat.id
    user_id = message.from_user.id
    fcx_user = db.User.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language
    wallet_address = message.text
    address_confirmation = {
        "en": f"""
Withdrawal Amount: <b>{amount}</b>
Payment Address: <b>{wallet_address}</b>
""",
        "it": f"""
Importo prelievo: <b>{amount}</b>
indirizzo di pagamento: <b>{wallet_address}</b>
        """
    }     
    bot.send_message(chat_id, text=address_confirmation[lang], parse_mode="html", reply_markup=confirm_order[lang])
                
#     address_confirmation = {
#             "en": f"""
# You're about to set your bitcoin wallet address to : 
# <strong>{wallet_address}</strong>
#             """,
#             "it": f"""
# Stai per impostare l'indirizzo del tuo portafoglio bitcoin su : 
# <strong>{wallet_address}</strong>
#             """
#     }    
#     bot.send_message(chat_id, text=address_confirmation[lang], parse_mode="html", reply_markup=confirm[lang])


def set_wallet_address(message):
    regex_filter = '^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$'
    chat_id = message.chat.id
    user_id = message.from_user.id
    fcx_user = db.User.get_user(user_id)
    lang = fcx_user.language
    wallet_address = message.text
    text_enter_address = {
        "en": """
<b>Please enter your Bitcoin wallet address:</b>
        """,
        "it": """
<b>Per favore inserire l’indirizzo del Vostro Wallet Bitcoin</b>
        """
    }
    bot.send_message(chat_id,text=text_enter_address[lang], parse_mode="html")
    bot.register_next_step_handler(message, wallet_address_confirmation)


@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and ( 
        bool(re.search(r'withdrawal$', message.text, re.IGNORECASE)) or 
        bool(re.search(r'Ritiro$', message.text, re.IGNORECASE))
        )
)
def withdrawal(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    message_id = message.message_id + 2
    fcx_user = db.User.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language
    withdrawal_minimum_amount = 0.002
    withdrawal_amount_text = {
        "en": """<b>Enter the amount you wish to withdraw</b>""",
        "it": """Enter the amount you wish to withdraw(italian"""
    }
    text_info = {
        "en": f"""
You can create a payout request any time, depending on your account balance.
Minimum amount to withdraw is 0.002 BTC.
        """,
        "it": f"""
E’ possibile fare una richiesta di pagamento in qualsiasi momento, a seconda del saldo del Vostro conto.
L’importo minimo di prelievo è di 0,002 BTC.
        """
        }
    text_insufficient = {
        "en": """
You don't have enough funds to create a payout request
        """,
        "it": """
Non avete abbastanza fondi per creare una richiesta di pagamento.
        """
    }
    if balance < withdrawal_minimum_amount:
        bot.send_message(
            chat_id, text=text_info[lang] + text_insufficient[lang],
            reply_markup=dashboard[lang], parse_mode="html"
            )
    else:
        bot.send_message(
            chat_id,  reply_to_message_id=message.message_id,
            text=text_info[lang],
            # reply_markup=force_r, 
            parse_mode="html"
            )
        bot.send_message(
            chat_id, 
            text=withdrawal_amount_text[lang], 
            parse_mode="html",
            reply_markup=force_r
            )
        bot.register_for_reply_by_message_id(message_id, wallet_amount_confirmation)
        # bot.register_next_step_handler(message, wallet_amount_confirmation)
    
