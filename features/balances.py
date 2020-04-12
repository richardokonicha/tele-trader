
from config import *

@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and (
        bool(re.search(r'^balance', message.text.split()[0], re.IGNORECASE)) or 
        bool(re.search(r'^bilance', message.text.split()[0], re.IGNORECASE))
        )
)
def balance(message):
    """Returns account balance report"""
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    fcx_user = db.User.get_user(user_id)
    if fcx_user is not None:
        if fcx_user.language not in ["en", "it"]:
            show_language(message)
        else:
            lang = fcx_user.language
            fcx_markup_balances = {
                        "en": f"Balance  {fcx_user.account_balance} BTC",
                        "it": f"Bilance  {fcx_user.account_balance} BTC"
                        }
            dashboard[lang].keyboard[0][0] = fcx_markup_balances[lang]

            try:
                balance = fcx_user.account_balance
                active_investment = fcx_user.active_investment
                active_reinvestment = fcx_user.active_reinvestment
                pending_investment = fcx_user.pending_investment
                
                balance_text = {

                "en": f"""
Your Account Balance:
<strong>{balance} BTC</strong>
Total Active Investments:
<strong>{active_investment} BTC</strong>
Total Active Reinvestments:
<strong>{active_reinvestment} BTC</strong>
Total Pending Investments:
<strong>{pending_investment} BTC</strong>
                """,

                "it": f"""


Saldo del conto:
<strong>{balance} BTC</strong>
Investimenti attivi:
<strong>{active_investment} BTC</strong>
Reinvestimenti attivi:
<strong>{active_reinvestment} BTC</strong>
Investimenti in sospeso:
<strong>{pending_investment} BTC</strong>


    """
                }
                if balance==0 and active_investment==0 and active_reinvestment==0 and pending_investment==0:
                    no_balance_text = {
                        "en": f"""
                            No investment yet. Go to <b>Deposit</b> to add funds.
                        """,
                        "it": f"""
                            Ancora nessun investimento
Andate a <b>Deposito</b> per aggiungere fondi.
                        """
                        }
                    bot.send_message( chat_id, text=no_balance_text[lang], reply_markup=dashboard.get(lang), parse_mode="html")
                else:
                    bot.send_message(chat_id, text=balance_text[lang], reply_markup=dashboard.get(lang), parse_mode="html")
            except KeyError:
                pass

    else:
        from starts import start
        start(message)