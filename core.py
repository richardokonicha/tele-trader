import telebot
import os
import requests
import re




fcx_markup = [
    [KeyboardButton(text='Balances 0.0000000 BTC', "bop")],
    ["Deposit", "Withdrawal"],
    ["Reinvest", "Transactions"],
    ["Team", "Settings", "Support"]
    ]

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
