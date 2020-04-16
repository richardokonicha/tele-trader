# Bot token provided by BotFather

# TOKEN_TEST = "852053528:AAHL_ryUUJ1JOhenzmI0WDiayAnxxqGFmyU"
# TOKEN = "746406709:AAHGsGOKxHwPOhRMdUOM5JNKsVxI2cCTbyQ" #fcxtrader bot
TOKEN_PRODUCTION = "1137661512:AAEig943WBK2aCBhlrDxgpN6Tl__lpxOMUY" #FCX trading bot

PUBLIC_KEY = "953b0c668c9d75c2d3da984f62a00fd269dc66c6da701250a0d7e14b52449183"
PRIVATE_KEY = "c68f21F77B13FE4D6617EfcD0287c036da7A3aB1A5f3e870fb179E940F5839Dd"
ipn_url="https://0218d890.ngrok.io/pay"

ADMIN_ID = 1053579181

TEST_URL = "https://cc0e3eb0.ngrok.io/"

PROD_URL = 'https://fcx-bot.herokuapp.com/'

try:
    import os
    DATABASE_URL = os.environ['DATABASE_URL']
except KeyError:
    DATABASE_URL="postgres://oilzaezgbpfuad:0c38dcf0bdd1cad9456aff15f7b6ae3cb076e5911dcbb5bf266afd5a3710e608@ec2-184-72-236-57.compute-1.amazonaws.com:5432/d3u443uoa0b5os"
    
