from config import *


############################### Start hander starts here ########################
@bot.message_handler(commands=["start"])
def start(message):
    """this is the starting point, it checks if user is not registered 
    and renders lang settings if user is registered uses pervious lang """
    chat_id = message.chat.id
    user_object = get_add_user(message)
    
    if user_object["lang"] not in ["ENGLISH", "ITALIAN"]:
        show_language(message)
    else:
        ####################################################################
        ####### Here is the welcome text users get each time they press start
        welcome_text = {

            "ENGLISH": """
                            <b>Welcome to FCX Trading Bot</b>

                    FCX Trading Bot is one of the most innovative Crypto and Forex trading providers.

                    Successful traders, now allow access to the financial world not only for big investors but also for the average person. 
                    With the simplified interface of the FCX Trading Bot, investing has never been
                    this easy to handle.

                    FCX Trading Bot profits depends on the global market situation and there is no guarantee of a fixed percentage of interest.
                    Our strategy is to generate profits at the lowest possible risk.

                    Deposits are being handled at the highest security level according
                    to a modern portfolio management serving the FCX Trading Bot.
                                    """,


            "ITALIAN": """
                            <b>Benvenuti a FCX Trading Bot </b>

                    FCX Trading Bot è uno dei più innovativi fornitori di Crypto e Forex trading. I trader di successo ora permettono l'accesso 
                    al mondo finanziario non solo ai grandi investitori ma anche alla persona media. Con l'interfaccia semplificata del FCX Trading Bot 
                    l'investimento non è mai stato così facile da gestire.

                    I profitti del FCX Trading Bot dipendono dalla situazione del mercato globale e non c'è garanzia di una percentuale fissa di interessi.
                    La nostra strategia è quella di generare profitti al minor rischio possibile.

                    I depositi sono gestiti al più alto livello di sicurezza secondo una moderna gestione di portafoglio al servizio del Trading Bot FCM.

                                    """
            }
        bot.send_message(
            chat_id,
            text=welcome_text[user_object["lang"]],
            reply_markup=home_keys,
            parse_mode="HTML"
            )
############################### Start handler ends here ########################

#
#
############################ language options starts here ###################
@bot.message_handler(
    func=lambda message: message.content_type == "text"
    and bool(re.search('^language$', message.text, re.IGNORECASE))
)
@bot.message_handler(commands=["language", "lang"])
def show_language(message):
    chat_id = message.chat.id
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
############################ language options ends here ###################



############################ language setter starts here ###################
@bot.message_handler(
    func=lambda message: message.text.split()[0] in ["English", "Italian"]
    # message.content_type == 'text' and 
    )
def set_langauge(message):
    """sets language and returns language value and send user confirmation message"""
    chat_id = message.chat.id
    user_object = get_user(message)
    message_lang = message.text.split()[0].upper()
    language = set_lang(user_object["user_id"], message_lang)
    set_lang_text = {
        "ENGLISH": """Language is set to: English 🇬🇧""",
        "ITALIAN": """La lingua è impostata su: Italian 🇮🇹"""
    }
    bot.send_message(
        chat_id,
        text=set_lang_text[language],
        reply_markup=home_keys
    )
############################ language setter ends here ###################



############################### Balance button handler ###################333

@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and bool(re.search(r'^balance[s.]', message.text, re.IGNORECASE))
)

def balances(message):
    """Returns account balance report"""
    
    chat_id = message.chat.id
    user_object = get_user(message)
    if user_object["lang"] not in ["ENGLISH", "ITALIAN"]:
        show_language(message)
    else:
        lang = user_object["lang"]

        try:
            balance = user_object["investment"]['balance']
            active_investment = user_object["investment"]['active_investment']
            active_reinvestment = user_object["investment"]['active_reinvestment']
            pending_investment = user_object["investment"]['pending_investment']
            
            
            balance_text = {

            "ENGLISH": f"""


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

            "ITALIAN": f"""


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
            bot.send_message(chat_id, text=balance_text[lang], reply_markup=home_keys, parse_mode="html")
        except KeyError:
            no_balance_text = {
                "ENGLISH": f"""
                    No investment yet. Go to <b>Deposit</b> to add funds.
                """,
                "ITALIAN": f"""
                    Ancora nessun investimento. Andate a Deposito per aggiungere fondi.
                """
                }
            bot.send_message( chat_id, text=no_balance_text[lang], reply_markup=home_keys, parse_mode="html")


############################################## Balance button handler ends here ################





########################################### Withdrawal handler starts here ######################
@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and bool(re.search(r'^withdrawal$', message.text.split()[1], re.IGNORECASE))
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
    if balance < withdrawal_minimum_amount:
        bot.send_message(
            chat_id, text=text_info[lang] + text_insufficient[lang],
            reply_markup=home_keys, parse_mode="html"
            )
    else:
        bot.send_message(
            chat_id, text=text_info[lang] + text_enter_address[lang],
            reply_markup=home_keys, parse_mode="html"
            )
        


############################### Withdrawal handler ends here #######################33





############################## DEPOSIT handler starts here ########################3
@bot.message_handler(
    func=lambda message: message.content_type == "text"
    and bool(re.search(r'^deposit$', message.text.split()[1], re.IGNORECASE))
)
def deposit(message):
    chat_id = message.chat.id
    user_object = get_user(message)
    balance = user_object["investment"]['balance']
    lang = user_object["lang"]
    wait_text = """
Please wait for our system to generate your New Deposit Address.
    """
    bot.send_message(
        chat_id, text=wait_text,
        reply_markup=home_keys, parse_mode="html"
        )
    bot.send_chat_action(chat_id, action="typing")
