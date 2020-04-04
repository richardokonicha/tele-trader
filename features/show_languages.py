
from config import *
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