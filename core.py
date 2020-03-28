import telebot
import os
import requests
import re
from telebot import types


fcx_markup = [
    ['Balances 0.0000000 BTC'],
    ["Deposit", "Withdrawal"],
    ["Reinvest", "Transactions"],
    ["Team", "Settings", "Support"]
    ]


welcome_text = """
        <b>Welcome to FCX Trading Bot</b>

FCX Trading Bot is one of the most innovative Crypto and Forex trading providers.

Successful traders, now allow access to the financial world not only for big investors but also for the average person. 
With the simplified interface of the FCX Trading Bot, investing has never been
this easy to handle.

FCX Trading Bot profits depends on the global market situation and there is no guarantee of a fixed percentage of interest.
Our strategy is to generate profits at the lowest possible risk.

Deposits are being handled at the highest security level according
to a modern portfolio management serving the FCX Trading Bot.

                """



def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url


def get_url():
    content = requests.get('https://random.dog/woof.json')
    url = content.json()["url"]
    return url


def bop(bot, updater):
    url = get_image_url()
    chat_id = updater.message.chat.id
    bot.send_photo(chat_id, photo=url)
