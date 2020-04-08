
from config import *

@bot.message_handler(
    func=lambda message: message.content_type == "text"
    and (
        bool(re.search(r'deposit$', message.text, re.IGNORECASE)) or 
        bool(re.search(r'Depositare$', message.text, re.IGNORECASE))
        )
)
def deposit(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    fcx_user = db.User.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language
    dashboard[lang].keyboard[0][0] = f"Balances  {fcx_user.account_balance} BTC"



    wait_text = {
        "en": """Please wait for our system to generate your New Deposit Address.""",
        "it": """Si prega di attendere che il nostro sistema generi il Vostro nuovo indirizzo di deposito."""
    }
    arrival_text = {
        "en": """Here is your personal BTC address for your Investments:""",
        "it": """Qui il Vostro indirizzo personale Bitcoin per i Vostri investimenti:"""
    }
    duration_text = {
        "en": """
Bitcoin Amount:
Min: 0.025 BTC
Max: 5 BTC

This address will be active for 4 hours.
Funds will show up after first blockchain confirmation.
""",
        "it": """
Importo Bitcoin: 
Min. 0,025 BTC 
Max. 5 BTC

Questo indirizzo sarà attivo per 4 ore.
I fondi appariranno dopo la prima conferma della Blockchain.
        
        """
    }
    bot.send_message(
        chat_id, text=wait_text.get(lang),
        parse_mode="html"
        )
    bot.send_chat_action(chat_id, action="typing")
   
    # try:
    # except KeyError:
    #     text = "Error occurred please contact by clicking the SUPPORT button"
    # text = "Error occurred please contact by clicking the SUPPORT button"

    bot.send_message(
        chat_id, text=arrival_text.get(lang)
    )
    payment_details = payment_client.get_callback_address(
        params={'currency': 'BTC'})

    try:

        text = payment_details["result"]["address"]

        bot.send_message(
            chat_id,
            text=f"<strong>{text}</strong>",
            parse_mode="html"
        )
        bot.send_message(
            chat_id,
            text=duration_text.get(lang),
            reply_markup=dashboard.get(lang)
        )
    
    except TypeError:
        fcx_user.account_balance = 0.1 # REMOVE THIS
        fcx_user.commit()
        dashboard[lang].keyboard[0][0] = f"Balances  {fcx_user.account_balance} BTC"
        bot.send_message(
            chat_id,
            text="error occured you'll be contacted by support, you've been gifted 0.10 virtual btc to test other features",
            reply_markup=dashboard.get(lang)
        )
        text = payment_details["error"]
        bot.send_message(
            ADMIN_ID,
            text=f"<strong>{text} for fcx server</strong>",
            parse_mode="html"
        )

