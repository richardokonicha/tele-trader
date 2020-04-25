# Bot token provided by BotFather

# TOKEN_TEST = "852053528:AAHL_ryUUJ1JOhenzmI0WDiayAnxxqGFmyU"
from sqlalchemy import create_engine

PUBLIC_KEY = "953b0c668c9d75c2d3da984f62a00fd269dc66c6da701250a0d7e14b52449183"
PRIVATE_KEY = "c68f21F77B13FE4D6617EfcD0287c036da7A3aB1A5f3e870fb179E940F5839Dd"
Merchant_ID = "c4baf6ef23be73a2da7fa0531b2df323"
IPN_secret = "coinpaymentspeaks"
ADMIN_ID = 1053579181
DEBUG = True

if DEBUG==False:
    print("\033[1;35;40m Running in production mode")
    TOKEN = "1137661512:AAEig943WBK2aCBhlrDxgpN6Tl__lpxOMUY" #FCX trading bot
    URL = 'https://fcx-trading.herokuapp.com/'
    try:
        import os
        DATABASE_URL = os.environ['DATABASE_URL']
    except KeyError:
        DATABASE_URL="postgres://oilzaezgbpfuad:0c38dcf0bdd1cad9456aff15f7b6ae3cb076e5911dcbb5bf266afd5a3710e608@ec2-184-72-236-57.compute-1.amazonaws.com:5432/d3u443uoa0b5os"
    db_url = DATABASE_URL.split(":")

    DATABASE_URI_VAR =f'postgres+psycopg2:{db_url[1]}:{db_url[2]}:{db_url[3]}'
    engine = create_engine(DATABASE_URI_VAR, echo=True)
    print(engine)

else:
    print("\033[1;32;40m Running in Development mode")
    TOKEN = "852053528:AAHL_ryUUJ1JOhenzmI0WDiayAnxxqGFmyU"

    # TOKEN = "746406709:AAHGsGOKxHwPOhRMdUOM5JNKsVxI2cCTbyQ" #fcxtrader bot
    URL = "https://f906f1e5.ngrok.io/"
    DATABASE_URL = 'postgres+psycopg2://postgres:postgres@localhost:5432'
    ADMIN_ID = 1053579181

    SQLITE = 'sqlite:///database/database.db'
    engine = create_engine(SQLITE, echo=True, connect_args={'check_same_thread': False})
    print(engine)

