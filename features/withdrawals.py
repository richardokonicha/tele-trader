from config import *


en_confirm_markup = types.InlineKeyboardMarkup(row_width=2)
it_confirm_markup = types.InlineKeyboardMarkup()

en_confirm_btn = types.InlineKeyboardButton(text="Confirm", callback_data="confirm_address")
en_modify_btn = types.InlineKeyboardButton(text="Cancel", callback_data="cancel_address")

it_confirm_btn = types.InlineKeyboardButton(text="Confermare", callback_data="confirm_address")
it_modify_btn = types.InlineKeyboardButton(text="Annulla", callback_data="cancel_address")

# en_confirm_markup.keyboard = [[en_confirm_btn], [en_modify_btn]]
# it_confirm_markup.keyboard = [[it_confirm_btn], [it_modify_btn]]

en_confirm_markup.add(en_confirm_btn, en_modify_btn)
it_confirm_markup.add(it_confirm_btn, it_modify_btn)


confirm = {
    "ENGLISH": en_confirm_markup,
    "ITALIAN": it_confirm_markup
}



# Callback Handlers
@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    chat_id = call.message.chat.id
    user_object = get_user_from_call(call.message)
    lang = user_object["lang"]
    wallet_address = call.message.text
    if call.data == "confirm_address":
        
        data = {
            "Withdrawals": {
                "wallet_address": wallet_address.split("\n")[1],
            }
        }
        update_user(user_object["user_id"], data)
        
        confirmation = {
                "ENGLISH": f"""
Your bitcoin wallet address has been set to : 
<strong>{wallet_address}</strong>
                """,
                "ITALIAN": f"""
Your bitcoin wallet address has been set to (italian) : 
<strong>{wallet_address}</strong>
                """
        }
        bot.send_message(chat_id, text=confirmation[lang], parse_mode="html", reply_markup=dashboard[lang])

    elif call.data == "cancel_address":
        bot.send_message(chat_id, text="not set", reply_markup=dashboard[lang])



def wallet_amount_confirmation(message):
    user_object = get_user(message)
    lang = user_object["lang"]
    chat_id = message.chat.id
    amount = message.text


def wallet_address_confirmation(message):
    user_object = get_user(message)
    lang = user_object["lang"]
    chat_id = message.chat.id
    wallet_address = message.text

    address_confirmation = {
            "ENGLISH": f"""
You're about to set your bitcoin wallet address to : 
<strong>{wallet_address}</strong>
            """,
            "ITALIAN": f"""
You're about to set you bitcoin wallet address to (italian) : 
<strong>{wallet_address}</strong>
            """
    }
    
    # bot.send_message(chat_id, text=address_confirmation[lang])
    bot.send_message(chat_id, text=address_confirmation[lang], parse_mode="html", reply_markup=confirm[lang])




@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and ( 
        bool(re.search(r'withdrawal$', message.text, re.IGNORECASE)) or 
        bool(re.search(r'Ritiro$', message.text, re.IGNORECASE))
        )
)
def withdrawal(message):
    chat_id = message.chat.id
    user_object = get_user(message)
    balance = user_object["investment"]['balance']
    lang = user_object["lang"]
    withdrawal_minimum_amount = 0.002


    withdrawal_amount_text = {
        "ENGLISH": """<b>Enter the amount you wish to withdraw</b>""",
        "ITALIAN": """Enter the amount you wish to withdraw(italian"""
    }
    ################
    text_info = {
        "ENGLISH": f"""
You can create a payout request any time, depending on your account balance.
Minimum amount to withdraw is 0.002 BTC.
        """,
        "ITALIAN": f"""
E’ possibile fare una richiesta di pagamento in qualsiasi momento, a seconda del saldo del Vostro conto.
L’importo minimo di prelievo è di 0,002 BTC.
        """
        }
    text_insufficient = {
        "ENGLISH": """
You don't have enough funds to create a payout request
        """,
        "ITALIAN": """
Non avete abbastanza fondi per creare una richiesta di pagamento.
        """
    }
    text_enter_address = {
        "ENGLISH": """
<b>Please enter your Bitcoin wallet address:</b>
        """,
        "ITALIAN": """
<b>Per favore inserire l’indirizzo del Vostro Wallet Bitcoin</b>
        """
    }

    if balance < withdrawal_minimum_amount:
        bot.send_message(
            chat_id, text=text_info[lang] + text_insufficient[lang],
            reply_markup=confirm, parse_mode="html"
            )
    else:
        bot.send_message(
            chat_id,  reply_to_message_id=message.message_id,
            text=text_info[lang],
            # reply_markup=force_r, 
            parse_mode="html"
            )

        bot.send_message(chat_id, text=withdrawal_amount_text[lang], parse_mode="html")
        bot.register_next_step_handler(message, wallet_amount_confirmation)

        
        # bot.send_message(chat_id,text=text_enter_address[lang], parse_mode="html")
        # bot.register_next_step_handler(message, wallet_address_confirmation)



