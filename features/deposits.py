
from config import *


def generate_address(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    fcx_user = db.User.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language
    try:

        amount = Decimal(message.text)
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
        if amount < 5:
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
            # payment_details = payment_client.create_transaction({"amount":amount, "currency1":"LTCT", "currency2":"LTCT"})
            payment_details = payment_client.create_transaction({"amount":amount, "currency1":"LTCT", "currency2":"LTCT"})

            try:
                pd = payment_details["result"]
                fcx_dp = db.Transactions(
                    user_id=fcx_user.user_id,
                    transaction_type="deposit",
                    amount = pd["amount"]
                )
                fcx_dp.dp_txn_id=pd["txn_id"]
                fcx_dp.dp_address_timeout = pd["timeout"]
                fcx_dp.dp_qrcode_url = pd["qrcode_url"]
                fcx_dp.dp_status = pd["status_url"]
                fcx_dp.dp_address = pd["address"]
                fcx_dp.status = "created"
                fcx_dp.commit()
                text = pd["address"]
                bot.send_message(
                    chat_id,
                    text=f"<strong>{text}</strong>",
                    parse_mode="html"
                )
                bot.send_photo(
                    chat_id,
                    photo=fcx_dp.dp_qrcode_url,
                    caption="Scan QR",
                )
                bot.send_message(
                    chat_id,
                    text=duration_text.get(lang),
                    reply_markup=dashboard.get(lang)
                )
            except TypeError:
                bot.send_message(
                    chat_id,
                    text="An error occured you'll be contacted by support to assit you.",
                    reply_markup=dashboard.get(lang)
                )
                text = payment_details["error"]
                bot.send_message(
                    ADMIN_ID,
                    text=f"<strong>{text} for fcx server</strong>",
                    parse_mode="html"
                )
        else:
            text = {
                "en": """<b>Maximum amount allowed is 5BTC</b>""",
                "it": """Maximum amount allowed is 5BTC (italian)"""
            }
            bot.send_message(
                chat_id,
                text=text,
                reply_markup=dashboard[lang]
            )
    except (ValueError, InvalidOperation) as e:
        bot.send_message(
            chat_id, 
            text="Invalid amount",
            reply_markup=dashboard[lang]
        )

#######################################DEPOSIT HANDLERS ##############################################
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
    message_id = message.message_id
    deposit_amount_text = {
        "en": """<b>Enter the amount you wish to deposit</b>""",
        "it": """Enter the amount you wish to deposit(italian"""
    }
    bot.send_message(
        chat_id,
        text=deposit_amount_text[lang],
        parse_mode="html",
        reply_markup=force_r
    )
    nxt = message_id + 1
    bot.register_for_reply_by_message_id(
        nxt,
        generate_address
    )


### Promo code section
@bot.message_handler(
    func=lambda message: message.content_type == "text"
    and (
        bool(re.search(r'^PROMO', message.text, re.IGNORECASE))
        )
)
def promo(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    fcx_user = db.User.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language
    dashboard[lang].keyboard[0][0] = f"Balances  {fcx_user.account_balance} BTC"
    promo = message.text.split(" ")[-1]
    try:
        promo = Decimal(promo)
        fcx_user.account_balance = fcx_user.account_balance + promo # REMOVE THIS
        fcx_transact = db.Transactions(
            fcx_user.user_id,
            transaction_type="deposit",
            amount=promo,
            status="Completed",
            balance=fcx_user.account_balance
            )
        fcx_transact.commit()
        dashboard[lang].keyboard[0][0] = f"Balances  {fcx_user.account_balance} BTC"
        bot.send_message(
            chat_id,
            text=f"You've been gifted {promo} virtual btc to test other features",
            reply_markup=dashboard.get(lang)
        )
    except ValueError:
        bot.send_message(
            chat_id,
            text="INVALID PROMO CODE",
            reply_markup=dashboard.get(lang)
        )