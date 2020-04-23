from config import *

@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and ( 
        bool(re.search(r'Support$', message.text, re.IGNORECASE))
         or  bool(re.search(r'Supporto$', message.text, re.IGNORECASE))
        )
)
def support(message):
    user_id = message.from_user.id
    fcx_user = db.User.get_user(user_id)
    lang = fcx_user.language
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
        user_id, text=text_info[lang],
        reply_markup=dashboard.get(lang), parse_mode="html"
        )

