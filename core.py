import telebot
import os
import requests
import re
from telebot import types

######### keyboard markup below here #######

from telebot import types
keys = types.ReplyKeyboardMarkup()


select_lang_markup = [
    ["ENGLISH", "ITALIAN"]
]

fcx_markup = [
    ["Balances BTC"],
    ["Deposit", "Withdrawal"],
    ["Reinvest", "Transactions"],
    ["Team", "Settings", "Support"]
    ]
######### keyboard markup above here #######




######### Test responses below here ###########



responses = {
    "select_prefered_lang": """Select your prefered language""",

    "set_lang_text": {
        "ENGLISH": """Your language has been set to ENGLISH you can change this anytime by going to setting from the main menu""",
        "ITALIAN": """je suis italian yeapp """
    },

    ####################################################################
    ###### Here is the welcome text users get each time they press start
    "welcome_text": {

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
    },



    #######################################################################
    ############## Balance text and no active balance text ###########
    # 
    
    # "balance_text": {

    #     "ENGLISH": f"""
    #                 Your account balance is {balance} BTC
    #                 Your active investments is {active_investment} BTC
    #                 Your active reinvestments is {active_reinvestment} BTC
    #                 Your pending investments is {pending_investment} BTC
    #     """,

    #     "ITALIAN": f"""
    #     Il saldo del tuo account è {balance} BTC
    #     I tuoi investimenti attivi sono {active_investment} BTC
    #     I tuoi reinvestimenti attivi sono {active_reinvestment} BTC
    #     I tuoi investimenti in sospeso sono {pending_investment} BTC


    #     """
    # },

    # "no_balance_text": {
    #     "ENGLISH": f"""
    #         No investment yet. Go to Deposit to add funds.
    #     """,
    #     "ITALIAN": f"""
    #         Ancora nessun investimento. Andate a Deposito per aggiungere fondi.
    #     """
    # }

}



# welcome_text = """
#         <b>Welcome to FCX Trading Bot</b>

# FCX Trading Bot is one of the most innovative Crypto and Forex trading providers.

# Successful traders, now allow access to the financial world not only for big investors but also for the average person. 
# With the simplified interface of the FCX Trading Bot, investing has never been
# this easy to handle.

# FCX Trading Bot profits depends on the global market situation and there is no guarantee of a fixed percentage of interest.
# Our strategy is to generate profits at the lowest possible risk.

# Deposits are being handled at the highest security level according
# to a modern portfolio management serving the FCX Trading Bot.

#                 """

####### Text responses above here #############
