
from config import *

@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and (
        bool(re.search(r'^balance[s.]', message.text.split()[0], re.IGNORECASE)) or 
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
            select_prefered_lang = """
Please select your language
Seleziona la tua lingua preferita
    """     
            bot.send_message(
                chat_id,
                text=select_prefered_lang,
                reply_markup=lang_keys,
                parse_mode="HTML"
                )
        else:
            lang = fcx_user.language
            dashboard[lang].keyboard[0][0] = f"Balances  {fcx_user.account_balance} BTC"



        # user_object = get_user(message)
        # if user_object["lang"] not in ["ENGLISH", "ITALIAN"]:
        #     show_language(message)
        # else:
        #     lang = user_object["lang"]

            try:
                balance = fcx_user.account_balance
                active_investment = fcx_user.active_investment
                active_reinvestment = fcx_user.active_reinvestment
                pending_investment = fcx_user.pending_investment


                # balance = user_object["investment"]['balance']
                # active_investment = user_object["investment"]['active_investment']
                # active_reinvestment = user_object["investment"]['active_reinvestment']
                # pending_investment = user_object["investment"]['pending_investment']
                
                
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

Base rate: 0.2% per day.
You may add another investment by pressing the <strong>DEPOSIT</strong> button. Your Balance will be grow up according Base rate and your Referrals.
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

Tariffa base: 0,2% al giorno.
È possibile aggiungere un altro investimento premendo il pulsante <strong>DEPOSIT</strong>. Il tuo saldo crescerà in base alla tariffa base e ai tuoi referral.        


    """
                }
                bot.send_message(chat_id, text=balance_text[lang], reply_markup=dashboard.get(lang), parse_mode="html")
            except KeyError:
                no_balance_text = {
                    "en": f"""
                        No investment yet. Go to <b>Deposit</b> to add funds.
                    """,
                    "it": f"""
                        Ancora nessun investimento. Andate a Deposito per aggiungere fondi.
                    """
                    }
                bot.send_message( chat_id, text=no_balance_text[lang], reply_markup=dashboard.get(lang), parse_mode="html")

    else:
        # dashboard[lang].keyboard[0][0] = f"Balances  {fcx_user.account_balance} BTC"
        # name = message.from_user.first_name
        # fcx_user = db.User(
        #     name=name,
        #     user_id=user_id
        # )
        # show_languages.show_language(message)
        # lang = fcx_user.language
        # fcx_user.commit()

        # bot.send_message(
        #     chat_id,
        #     text=welcome_text[lang],
        #     reply_markup=dashboard[lang],
        #     parse_mode="HTML"
        #     )
        from starts import start
        start(message)