#%%

import re

import requests
from telegram.ext import CommandHandler, Updater
from telegram import ReplyKeyboardMarkup, KeyboardButton

Bot_token = "746406709:AAHGsGOKxHwPOhRMdUOM5JNKsVxI2cCTbyQ"


fcx_markup = [
    [KeyboardButton(text='Balances 0.0000000 BTC', "bop")],
    ["Deposit", "Withdrawal"],
    ["Reinvest", "Transactions"],
    ["Team", "Settings", "Support"]
    ]


keys = ReplyKeyboardMarkup(keyboard=fcx_markup, resize_keyboard=True)

# keys_func = ReplyKeyboardMarkup.from_column(
#     ["['/bop', 'ITALIAN', telegram.KeyboardButton(text='Logo')]", "cheaphhhhh skirt"],
#     resize_keyboard=True
#     )


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


def trader(bot, updater):
    text = "this is really fun"
    chat_id = 1053579181
    bot.send_message(chat_id, text=text, reply_markup=keys)


def main():
    # import pdb; pdb.set_trace()
    updater = Updater(Bot_token)
    my_dispatcher = updater.dispatcher
    my_dispatcher.add_handler(CommandHandler('bop', bop))
    my_dispatcher.add_handler(CommandHandler('trader', trader))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()



