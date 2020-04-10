from config import *

@bot.message_handler(
    func=lambda message: message.text.split()[0] in ["English", "Italian"]
    # message.content_type == 'text' and 
    )
def set_langauge(message):
    """sets language and returns language value and send user confirmation message"""
    chat_id = message.chat.id
    user_id = message.from_user.id
    fcx_user = db.User.get_user(user_id)
    message_lang = message.text.split()[0].upper()
    if message_lang == "ENGLISH":
        fcx_user.language = 'en'
    if message_lang == "ITALIAN":
        fcx_user.language = "it"
    lang = fcx_user.language
    fcx_user.commit()
    set_lang_text = {
        "en": """Language is set to: English 🇬🇧""",
        "it": """La lingua è impostata su: Italian 🇮🇹"""
    }
    bot.send_message(
        chat_id,
        text=set_lang_text[lang],
        reply_markup=dashboard[lang]
    )
    # take user back to start
    if fcx_user.is_new_user:
        import starts
        starts.start(message)
