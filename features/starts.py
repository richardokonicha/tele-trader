
from config import *
import sys
import database as dba

@bot.message_handler(commands=["start"])
def start(message):
    """this is the starting point, it checks if user is not registered 
    and renders lang settings if user is registered uses pervious lang """
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.first_name

    fcx_user = db.User(
        name=name,
        user_id=user_id
    )

    
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