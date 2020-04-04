
from config import *

@bot.message_handler(
    func=lambda message: message.content_type == 'text'
    and ( 
        bool(re.search(r'^Team$', message.text, re.IGNORECASE))
         or  bool(re.search(r'^Squadra$', message.text, re.IGNORECASE))
        )
)
def team(message):
    chat_id = message.chat.id
    user_object = get_user(message)
    balance = user_object["investment"]['balance']
    lang = user_object["lang"]
    withdrawal_minimum_amount = 0.002
    text_info = {
        "ENGLISH": f"""
Invitation link to share with your friends:
        """,
        "ITALIAN": f"""
Link di invito da condividere con i Vostri amici:
        """
        }
        
    text_refferal = {
        "ENGLISH": """

Refferal system:
1. Level 5%
2. Level 3%
3. Level 1%

Team:
1. Level partner: 10
2. Level partner:  5
3. Level partner:  2

Team volume:
1. Level: 1.000000 BTC
2. Level  0.557777 BTC
3. Level  0.236675 BTC

Total team earnings:
xx.xxxxxx BTC


        """,
        "ITALIAN": """

Livelli Bonus:
1. Livello 5%
2. Livello 3%
3. Livello 1%

Team:
1. Partner di livello: 10
2. Partner di livello: 5
3. Partner di livello: 2

Totale della squadra:
1. Livello: 1.000000 BTC
2. Livello 0,557777 BTC
3. Livello 0,236675 BTC


Guadagno totale della squadra:
xx.xxxxxx BTC
        """
    }
    text_enter_commission = {
        "ENGLISH": """
Your commissions will be added automatically to your main account balance each time a team member makes a deposit or a reinvestment.
        """,
        "ITALIAN": """
Le Vostre commissioni saranno aggiunte automaticamente al saldo del Vostro conto principale ogni volta che un membro del team effettua un deposito o un reinvestimento. 
        """
    }
    bot.send_message( chat_id, text=text_info[lang] + text_refferal[lang] + text_enter_commission[lang],
        reply_markup=dashboard.get(lang), parse_mode="html"
        )

