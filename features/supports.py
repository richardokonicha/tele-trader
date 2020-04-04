from config import *

@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and ( 
        bool(re.search(r'Support$', message.text, re.IGNORECASE))
         or  bool(re.search(r'Supporto$', message.text, re.IGNORECASE))
        )
)
def support(message):
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

