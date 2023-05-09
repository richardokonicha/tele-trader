from sqlalchemy import create_engine

DEBUG = True
if DEBUG == False:
    print("\033[1;35;40m Running in production mode")
    TOKEN = "852053528:AAEOdgDErcNtHbbK2E-80uSFmF5tsCeJdSc"  # FCX trading bot
    URL = 'https://8828-richardokoni-teletrader-1q4ifr00tyi.ws-eu96b.gitpod.io/'
    try:
        import os
        DATABASE_URL = os.environ['DATABASE_URL']
    except KeyError:
        DATABASE_URL = "postgres://default:HlJzr0v6eyGp@ep-calm-brook-757839.us-east-1.postgres.vercel-storage.com:5432/verceldb"
    db_url = DATABASE_URL.split(":")
    DATABASE_URI_VAR = f'postgres+psycopg2:{db_url[1]}:{db_url[2]}:{db_url[3]}'
    engine = create_engine(DATABASE_URI_VAR, echo=True)
    print(engine)
else:
    print("\033[1;32;40m Running in Development mode")
    TOKEN = "852053528:AAEOdgDErcNtHbbK2E-80uSFmF5tsCeJdSc"
    URL = 'https://5000-richardokoni-teletrader-1q4ifr00tyi.ws-eu96b.gitpod.io/'
    ADMIN_ID = 1053579181
    SQLITE = 'sqlite:///database/database.db'
    engine = create_engine(SQLITE, echo=True, connect_args={
                           'check_same_thread': False})
    print(engine)
