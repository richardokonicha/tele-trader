
from config import *

@bot.message_handler(commands=["start"])
def start(message):
    """this is the starting point, it checks if user is not registered 
    and renders lang settings if user is registered uses pervious lang """
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.first_name
    welcome_text = {

            "en": """
                            <b>Welcome to FCX Trading Bot</b>

FCX Trading Bot is one of the most innovative Crypto and Forex trading providers. Successful traders, now allow access to the financial world not only for big investors but also for the average person. With the simplified interface of the FCX Trading Bot, investing has never been this easy to handle.

FCX Trading Bot profits depends on the global market situation and there is no guarantee of a fixed percentage of interest. Our strategy is to generate profits at the lowest possible risk.

Deposits are being handled at the highest security level according to a modern portfolio management serving the FCX Trading Bot.
                                    """,


            "it": """
                            <b>Benvenuti a FCX Trading Bot </b>

FCX Trading Bot è uno dei più innovativi fornitori di Crypto e Forex trading. I trader di successo ora permettono l'accesso al mondo finanziario non solo ai grandi investitori ma anche alla persona media. Con l'interfaccia semplificata del FCX Trading Bot l'investimento non è mai stato così facile da gestire.

I profitti del FCX Trading Bot dipendono dalla situazione del mercato globale e non c'è garanzia di una percentuale fissa di interessi. La nostra strategia è quella di generare profitti al minor rischio possibile.

I depositi sono gestiti al più alto livello di sicurezza secondo una moderna gestione di portafoglio al servizio del Trading Bot FCM.

                                """
            }
    fcx_user = db.User.get_user(user_id)

    if fcx_user is not None:
        lang = fcx_user.language
        if lang == None or lang not in ['en', 'it']:
            show_languages.show_language(message)
            fcx_user.commit()
        else:
            dashboard[lang].keyboard[0][0] = f"Balances  {fcx_user.account_balance} BTC"
            bot.send_message(
                chat_id,
                text=welcome_text[lang],
                reply_markup=dashboard[lang],
                parse_mode="HTML"
                )
    else:
        # for new users only
        select_prefered_lang = """
Please select your language
Seleziona la tua lingua preferita
    """
        fcx_user = db.User(
            name=name,
            user_id=user_id
        )
        fcx_user.is_new_user = True
        fcx_user.commit()
        bot.send_message(
            chat_id,
            text=select_prefered_lang,
            reply_markup=lang_keys,
            parse_mode="HTML"
            )

        # show_languages.show_language(message)
        # bot.send_message(
        #     chat_id,
        #     text=welcome_text[lang],
        #     reply_markup=dashboard[lang],
        #     parse_mode="HTML"
        #     )
        # lang = fcx_user.language
