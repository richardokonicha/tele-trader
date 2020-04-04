from config import *

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
Please enter your Bitcoin wallet address:
        """,
        "ITALIAN": """
Per favore inserire l’indirizzo del Vostro Wallet Bitcoin
        """
    }
    address_confirmation = {
            "ENGLISH": """
You're about to set your bitcoin wallet address to :
            """,
            "ITALIAN": """
You're about to set you bitcoin wallet address to (italian) : 
            """
    }



    if balance < withdrawal_minimum_amount:
        bot.send_message(
            chat_id, text=text_info[lang] + text_insufficient[lang],
            reply_markup=home_keys, parse_mode="html"
            )
    else:
        bot.send_message(
            chat_id, text=text_info[lang] + text_enter_address[lang],
            reply_markup=force_r, parse_mode="html"
            )
        bot.register_next_step_handler(message, wallet_address_confirmation(lang))



    def wallet_address_confirmation(message, lang):
            chat_id = message.chat.id
            user_wallet = message.text
            bot.send_message(chat_id, text=address_confirmation[lang] + user_wallet, reply_markup=dashboard.get(lang))



