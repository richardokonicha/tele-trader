import os
import psycopg2
from datetime import datetime, timedelta
from decimal import *

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, exists, update, DateTime, Numeric, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from settings import engine

# connect engine to the database 

# export DATABASE_URL=postgres://$(whoami)
# postgres://reechee
# DATABASE_URL='postgres://reechee'.split(":")
# DATABASE_URI_VARI = 'postgres+psycopg2://postgres:postgres@localhost:5432'
# Base.metadata.drop_all(engine)

# DATABASE_URI = 'postgres+psycopg2://reechee:reechee@localhost:5432'
# DATABASE_URL="postgres://oilzaezgbpfuad:0c38dcf0bdd1cad9456aff15f7b6ae3cb076e5911dcbb5bf266afd5a3710e608@ec2-184-72-236-57.compute-1.amazonaws.com:5432/d3u443uoa0b5os"
# engine = create_engine(DATABASE_URI, echo=True, connect_args={'check_same_thread': False})


# except KeyError:
#     DATABASE_URI = 'postgres+psycopg2://postgres:postgres@localhost:5432'
# export DATABASE_URL='postgres+psycopg2://postgres:postgres@localhost:5432'

# db_url = DATABASE_URL.split(":")
# DATABASE_URI_VAR =f'postgres+psycopg2:{db_url[1]}:{db_url[2]}:{db_url[3]}'
# engine = create_engine(DATABASE_URI_VAR, echo=True)

# SQLITE = 'sqlite:///database/database.db'
# engine = create_engine(SQLITE, echo=True, connect_args={'check_same_thread': False})

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
Base = declarative_base()


class Setup:
    # @classmethod
    def activate_db():
        Base.metadata.create_all(engine)
        return

    # @classmethod
    def test_users():
        test_user = User(user_id=7878, name="tester_org")
        test_user.commit()
        test_transact = Transactions(user_id=7878, transaction_type="withdrawal", amount=0.5)
        test_transact.commit()
        return

#  create a schema
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,  unique=True)
    name = Column(String, nullable=False)
    language = Column(String)
    referral = Column(String)
    registered_date = Column(String)
    is_new_user = Column(Boolean)
    last_visted = Column(String)
    wallet_address = Column(String)

    account_balance = Column(DECIMAL(8,6))
    active_investment = Column(DECIMAL(8,6))
    pending_investment = Column(DECIMAL(8,6))
    active_reinvestment = Column(DECIMAL(8,6))
    transactions = relationship("Transactions", uselist=True, backref="user")

    def __init__(self, user_id, name, is_admin=False, is_new_user=True):
        self.user_id = user_id
        self.name = name
        self.is_admin = is_admin
        self.is_new_user = is_new_user
        self.registered_date = datetime.now().isoformat()
        self.account_balance = Decimal()
        self.active_investment = Decimal()
        self.active_reinvestment = Decimal()
        self.pending_investment = Decimal()
        
    def exists(self):
        return session.query(exists().where(User.user_id == self.user_id)).scalar()

    @classmethod
    def exists_id(cls, user_id):
        return session.query(exists().where(cls.user_id == user_id)).scalar()

    @classmethod
    def get_user(cls, user_id):
        if session.query(exists().where(cls.user_id == user_id)).scalar():
            return session.query(cls).filter_by(user_id=user_id).first()
        else:
            return None

    def set_last_visted(self):
        self.last_visted = datetime.now().fromisoformat()
        return self.last_visted

    def commit(self):
        session.add(self)
        session.commit()

    def __repr__(self):
        return f"User {self.name}"

# then we create a session and bind to the engine

# then we create an instance of the mapped class

# To persist in memory our User object/instance, we add() it to our Session: At this point, we say that the instance is pending;

# test_user = User(name="test_user", language='en')

# session.add(test_user)
# session.commit()


class Transactions(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    transaction_type = Column(String)
    amount = Column(DECIMAL(8,6))
    wallet_address = Column(String)
    date = Column(String)
    start_date = Column(String)
    balance = Column(DECIMAL(8,6))
    # deposit
    dp_txn_id = Column(String, unique=True)
    dp_address = Column(String)
    dp_address_timeout = Column(Integer)
    dp_qrcode_url = Column(String)
    dp_status = Column(String)
    dp_status_text = Column(String)

    # users = relationship("User",uselist=True, back_populates="transaction")

    def __init__(
        self,
        user_id,
        transaction_type,
        amount,
        wallet_address=None,
        balance=None,
        status="Pending"
        ):
        self.user_id = user_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.wallet_address = wallet_address
        self.date = datetime.now().isoformat()
        self.start_date = datetime.now().replace(
            day=(datetime.now().day+(7-datetime.now().weekday()))
            ).isoformat()
        self.close_date = (
            datetime.now().replace(
                day=(datetime.now().day+(7-datetime.now().weekday()))
                ) + timedelta(days=180)
            ).isoformat()
        self.balance = balance
        self.status = status

    @classmethod
    def get_transactions(cls, user_id):
        transaction = session.query(cls).filter_by(user_id=user_id).all()
        if transaction:
            return transaction
        else:
            return None
    
    @classmethod
    def get_txn_id(cls, txn_id):
        return session.query(Transactions).filter_by(dp_txn_id=txn_id).first()
    
    def commit(self):
        session.add(self)
        session.commit()

    def start_date(self):
        return (self.start_date).isoformat().strftime("%A %d. %B %Y")
    
    def close_date(self):
        return (self.start_date + timedelta(days=180)).isoformat().strftime("%A %d. %B %Y")

    def __repr__(self):
        return f"Transaction {self.user_id} {self.transaction_type} {self.amount}"



# class Deposits(Base):
#     __tablename__="deposit"
#     id = Column(Integer, primary_key=True)
#     deposit_txn_id = Column(String)
#     amount = Column(Integer)
#     address = Column(String)
#     timeout = Column(Integer)
#     qrcode_url = Column(String)
#     status = Column(String)
#     date = Column(DateTime)



#     def commit(self):
#         session.add(self)
#         session.commit()
    
#     def __repr__(self):
#         return f"Deposit {self.txn_id} amount {self.amount}"


Base.metadata.create_all(engine)

