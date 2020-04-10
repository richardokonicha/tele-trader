
from config import *

# Callback Handlers
@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    fcx_user = db.User.get_user(user_id)
    balance = fcx_user.account_balance
    lang = fcx_user.language
    if call.data == "confirm_address":
        wallet_address = call.message.text.split('\n')[1]
        fcx_user.wallet_address = wallet_address
        fcx_user.commit()
        confirmation = {
                "en": f"""
Your bitcoin wallet address has been set to : 
<strong>{fcx_user.wallet_address}</strong>

You can now make a <b>withdrawal</b>
                """,
                "it": f"""
Il tuo indirizzo di portafoglio bitcoin è stato impostato su : 
<strong>{fcx_user.wallet_address}</strong>

Ora puoi effettuare un <b>prelievo</b>
                """
        }
        bot.send_message(chat_id, text=confirmation[lang], parse_mode="html", reply_markup=dashboard[lang])
    elif call.data == "cancel_address":
        bot.send_message(chat_id, text="cancelled", reply_markup=dashboard[lang])
    elif call.data == "confirm_order":
        withdrawal_order = call.message.text
        amount_text, address_text = withdrawal_order.split('\n')
        amount = float(amount_text.split(' ')[-1])
        wallet_address = address_text.split(' ')[-1]
        fcx_user.account_balance = fcx_user.account_balance - amount
        fcx_transact = db.Transactions(
            user_id = fcx_user.user_id,
            transaction_type="withdrawal",
            amount=amount,
            status="Pending",
            balance=fcx_user.account_balance,
            wallet_address=wallet_address
            )
        fcx_user.commit()
        fcx_transact.commit()
        order_set_text = {
            "en": f"""Your withdrawal order of 
<b>{amount_text}</b> 
would be credited to your account
<b>{address_text}</b> 
within the next 72 hours

Your new balance is {fcx_user.account_balance}""",
            "it": f"""Il tuo ordine di prelievo di
<b>{amount_text}</b> 
verrebbe accreditato sul tuo conto Indirizzo di pagamento:
<b>{address_text}</b>
entro le prossime 72 ore

Il tuo nuovo saldo è {fcx_user.account_balance}"""
        }
        bot.send_message(
            ADMIN_ID,
            text=withdrawal_order,
            parse_mode="html"
        )
        dashboard[lang].keyboard[0][0] = f"Balances  {fcx_user.account_balance} BTC"
        bot.send_message(
            chat_id, 
            text=order_set_text[lang], 
            parse_mode="html",
            reply_markup=dashboard[lang]
            )
        ##### REINVEST #####
    elif call.data == "confirm_reinvestment":
        amount = call.message.text.split(":")[-1]
        amount = float(amount.split(" ")[0])
        fcx_user.account_balance = fcx_user.account_balance - amount
        fcx_user.reinvestment = fcx_user.reinvestment + amount
        fcx_reinvest = db.Transactions(
            user_id=user_id,
            transaction_type="reinvestment",
            amount=amount,
            balance=balance,
            status="completed"
        )
        start_date = "Monday"
        fcx_reinvest.commit()
        confirm_reinvest_text = {
            "en": f"""
Done. Your reinvest starts {start_date}
            """,
            "it": f"""
Fatto. Il Vostro reinvestimento inizia il {start_date}
            """
        }
        bot.send_message(
            chat_id,
            text=confirm_reinvest_text[lang],
            reply_markup=dashboard[lang]
        )
