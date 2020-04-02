from config import *
from coinpayment import CoinPayments
payment_client = CoinPayments(PublicKey, PrivateKey)


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
        user_object = get_user(message)
        lang = user_object["lang"]
        ####################################################################
        ####### Here is the welcome text users get each time they press start
        welcome_text = {

            "ENGLISH": """
                            <b>Welcome to FCX Trading Bot</b>

FCX Trading Bot is one of the most innovative Crypto and Forex trading providers. Successful traders, now allow access to the financial world not only for big investors but also for the average person. With the simplified interface of the FCX Trading Bot, investing has never been this easy to handle.

FCX Trading Bot profits depends on the global market situation and there is no guarantee of a fixed percentage of interest. Our strategy is to generate profits at the lowest possible risk.

Deposits are being handled at the highest security level according to a modern portfolio management serving the FCX Trading Bot.
                                    """,


            "ITALIAN": """
                            <b>Benvenuti a FCX Trading Bot </b>

FCX Trading Bot è uno dei più innovativi fornitori di Crypto e Forex trading. I trader di successo ora permettono l'accesso al mondo finanziario non solo ai grandi investitori ma anche alla persona media. Con l'interfaccia semplificata del FCX Trading Bot l'investimento non è mai stato così facile da gestire.

I profitti del FCX Trading Bot dipendono dalla situazione del mercato globale e non c'è garanzia di una percentuale fissa di interessi. La nostra strategia è quella di generare profitti al minor rischio possibile.

I depositi sono gestiti al più alto livello di sicurezza secondo una moderna gestione di portafoglio al servizio del Trading Bot FCM.

                                    """
            }
        bot.send_message(
            chat_id,
            text=welcome_text[user_object["lang"]],
            reply_markup=dashboard[lang],
            parse_mode="HTML"
            )
############################### Start handler ends here ########################

#
#
############################ language options starts here ###################
@bot.message_handler(
    func=lambda message: message.content_type == "text"
    and (
        bool(re.search('^.+language', message.text, re.IGNORECASE)) or
        bool(re.search('^.+linguaggio', message.text, re.IGNORECASE)) 
        )
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
    lang = user_object["lang"]
    message_lang = message.text.split()[0].upper()
    language = set_lang(user_object["user_id"], message_lang)
    set_lang_text = {
        "ENGLISH": """Language is set to: English 🇬🇧""",
        "ITALIAN": """La lingua è impostata su: Italian 🇮🇹"""
    }
    bot.send_message(
        chat_id,
        text=set_lang_text[language],
        reply_markup=dashboard.get(language)
    )
############################ language setter ends here ###################



############################### Balance button handler ###################333

@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and (
        bool(re.search(r'^balance[s.]', message.text.split()[0], re.IGNORECASE)) or 
        bool(re.search(r'^bilance', message.text.split()[0], re.IGNORECASE))
        )
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
            bot.send_message(chat_id, text=balance_text[lang], reply_markup=dashboard.get(lang), parse_mode="html")
        except KeyError:
            no_balance_text = {
                "ENGLISH": f"""
                    No investment yet. Go to <b>Deposit</b> to add funds.
                """,
                "ITALIAN": f"""
                    Ancora nessun investimento. Andate a Deposito per aggiungere fondi.
                """
                }
            bot.send_message( chat_id, text=no_balance_text[lang], reply_markup=dashboard.get(lang), parse_mode="html")


############################################## Balance button handler ends here ################





########################################### Withdrawal handler starts here ######################
@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and ( 
        bool(re.search(r'^withdrawal$', message.text.split()[1], re.IGNORECASE)) or 
        bool(re.search(r'^Ritiro$', message.text.split()[1], re.IGNORECASE))
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
    if balance < withdrawal_minimum_amount:
        bot.send_message(
            chat_id, text=text_info[lang] + text_insufficient[lang],
            reply_markup=home_keys, parse_mode="html"
            )
    else:
        bot.send_message(
            chat_id, text=text_info[lang] + text_enter_address[lang],
            reply_markup=dashboard.get(lang), parse_mode="html"
            )



############################### Withdrawal handler ends here #######################33





############################## DEPOSIT handler starts here ########################3
@bot.message_handler(
    func=lambda message: message.content_type == "text"
    and (
        bool(re.search(r'^deposit$', message.text.split()[1], re.IGNORECASE)) or 
        bool(re.search(r'^Depositare$', message.text.split()[1], re.IGNORECASE))
        )
)
def deposit(message):
    chat_id = message.chat.id
    user_object = get_user(message)
    balance = user_object["investment"]['balance']
    lang = user_object["lang"]
    

    wait_text = {
        "ENGLISH": """Please wait for our system to generate your New Deposit Address.""",
        "ITALIAN": """Si prega di attendere che il nostro sistema generi il Vostro nuovo indirizzo di deposito."""
    }
    arrival_text = {
        "ENGLISH": """Here is your personal BTC address for your Investments:""",
        "ITALIAN": """Qui il Vostro indirizzo personale Bitcoin per i Vostri investimenti:"""
    }
    duration_text = {
        "ENGLISH": """
Bitcoin Amount:
Min: 0.025 BTC
Max: 5 BTC

This address will be active for 4 hours.
Funds will show up after first blockchain confirmation.
""",
        "ITALIAN": """
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

    print(payment_details)
    print(payment_details["result"])
    import pdb; pdb.set_trace()
    text = payment_details["result"]["address"]
    tex = payment_details["result"]
    print(tex)


    bot.send_message(
        chat_id,
        text=f"<strong>{text}{tex}</strong>",
        parse_mode="html"
    )
    bot.send_message(
        chat_id,
        text=duration_text.get(lang),
        reply_markup=dashboard.get(lang)
    )
    
#########################DEPOSIT HANDLER ENDS HERE ###########








########################################### Reinvest handler starts here ######################
@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and ( 
        bool(re.search(r'^Reinvest$', message.text.split()[1], re.IGNORECASE))
        #  or  bool(re.search(r'^Ritiro$', message.text.split()[1], re.IGNORECASE))
        )
)
def reinvest(message):
    chat_id = message.chat.id
    user_object = get_user(message)
    balance = user_object["investment"]['balance']
    lang = user_object["lang"]
    withdrawal_minimum_amount = 0.002
    text_info = {
        "ENGLISH": f"""
You can make a reinvest any time, depending on your account balance . 
Minimum amount to reinvest is 0.002 BTC. Once credited, each reinvestment counts for itself and runs for 180 days.
        """,
        "ITALIAN": f"""
Potete effettuare un reinvestimento in qualsiasi momento, a seconda del saldo del Vostro conto. L'importo minimo da reinvestire è di 0,002 BTC. Una volta accreditato, ogni reinvestimento vale per se stesso e dura 180 giorni.
        """
        }
    text_insufficient = {
        "ENGLISH": """
You don't have enough funds to create a reinvest
        """,
        "ITALIAN": """
Non avete abbastanza fondi per creare un reinvestimento. 
        """
    }
    text_enter_amount = {
        "ENGLISH": """
Please enter the amount to reinvest:
        """,
        "ITALIAN": """
Per favore inserire l'importo da reinvestire:
        """
    }
    if balance < withdrawal_minimum_amount:
        bot.send_message(
            chat_id, text=text_info[lang] + text_insufficient[lang],
            reply_markup=home_keys, parse_mode="html"
            )
    else:
        bot.send_message(
            chat_id, text=text_info[lang] + text_enter_amount[lang],
            reply_markup=dashboard.get(lang), parse_mode="html"
            )



############################### REinvest handler ends here #######################33




########################################### Team handler starts here ######################
@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and ( 
        bool(re.search(r'^Team$', message.text.split()[1], re.IGNORECASE))
         or  bool(re.search(r'^Squadra$', message.text.split()[1], re.IGNORECASE))
        )
)
def Team(message):
    chat_id = message.chat.id
    user_object = get_user(message)
    balance = user_object["investment"]['balance']
    lang = user_object["lang"]
    withdrawal_minimum_amount = 0.002
    text_info = {
        "ENGLISH": f"""
Invitation link to share with your friends:
        """,
        "ITALIAN": f"""
Link di invito da condividere con i Vostri amici:
        """
        }
        
    text_refferal = {
        "ENGLISH": """

Refferal system:
1. Level 5%
2. Level 3%
3. Level 1%

Team:
1. Level partner: 10
2. Level partner:  5
3. Level partner:  2

Team volume:
1. Level: 1.000000 BTC
2. Level  0.557777 BTC
3. Level  0.236675 BTC

Total team earnings:
xx.xxxxxx BTC


        """,
        "ITALIAN": """

Livelli Bonus:
1. Livello 5%
2. Livello 3%
3. Livello 1%

Team:
1. Partner di livello: 10
2. Partner di livello: 5
3. Partner di livello: 2

Totale della squadra:
1. Livello: 1.000000 BTC
2. Livello 0,557777 BTC
3. Livello 0,236675 BTC


Guadagno totale della squadra:
xx.xxxxxx BTC
        """
    }
    text_enter_commission = {
        "ENGLISH": """
Your commissions will be added automatically to your main account balance each time a team member makes a deposit or a reinvestment.
        """,
        "ITALIAN": """
Le Vostre commissioni saranno aggiunte automaticamente al saldo del Vostro conto principale ogni volta che un membro del team effettua un deposito o un reinvestimento. 
        """
    }
    bot.send_message( chat_id, text=text_info[lang] + text_refferal[lang] + text_enter_commission[lang],
        reply_markup=dashboard.get(lang), parse_mode="html"
        )



############################### Team handler ends here #######################33





########################################### Transaction handler starts here ######################
@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and ( 
        bool(re.search(r'^Transactions$', message.text.split()[1], re.IGNORECASE))
         or  bool(re.search(r'^Transazioni$', message.text.split()[1], re.IGNORECASE))
        )
)
def Transaction(message):
    chat_id = message.chat.id
    user_object = get_user(message)
    balance = user_object["investment"]['balance']
    lang = user_object["lang"]
    text_info = {
        "ENGLISH": f"""

Deposits:
.....
30/03/2020 0.022111 BTC 
23/03/2020 0.500000 BTC     


Payouts:
.....
30/04/2020 0.022111 BTC 
27/03/2020 0.500000 BTC


Reinvestments:
......
15/07/2020 0.500000 BTC
15/06/2020 0.022111 BTC

Commissions:
.....
17/08/2020 0.500000 BTC
08/06/2020 0.022111 BTC

        """,
        "ITALIAN": f"""
Depositi:
.....
30/03/2020 0,022111 BTC   
23/03/2020 0.500000 BTC 

Pagamenti:
.....
30/04/2020 0,022111 BTC
27/03/2020 0.500000 BTC

Reinvestimenti:
......
15/07/2020 0,500000 BTC
15/06/2020 0,022111 BTC

Commissioni:
.....
17/08/2020 0,500000 BTC
08/06/2020 0.022111 BTC 


        """
        }


    bot.send_message(
        chat_id, text=text_info[lang],
        reply_markup=dashboard.get(lang), parse_mode="html"
        )



############################### Transaction handler ends here #######################33






########################################### Support handler starts here ######################
@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and ( 
        bool(re.search(r'^Support$', message.text.split()[1], re.IGNORECASE))
         or  bool(re.search(r'^Supporto$', message.text.split()[1], re.IGNORECASE))
        )
)
def Support(message):
    chat_id = message.chat.id
    user_object = get_user(message)
    balance = user_object["investment"]['balance']
    lang = user_object["lang"]
    text_info = {
        "ENGLISH": f"""
Contact:
@fcx_bot
        """,
        "ITALIAN": f"""
Contatto:
@fcx_bot

        """
        }

    bot.send_message(
        chat_id, text=text_info[lang],
        reply_markup=dashboard.get(lang), parse_mode="html"
        )



############################### Support handler ends here #######################33





