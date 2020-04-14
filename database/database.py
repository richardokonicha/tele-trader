from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, exists, update
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta


# connect engine to the database 



# connect engine to the database 

# export DATABASE_URL=postgres://$(whoami)

# DATABASE_URI = 'postgres+psycopg2://postgres:password@localhost:5432/books'
# Base.metadata.drop_all(engine)

import os
import psycopg2

# DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URI = 'postgres+psycopg2://reechee:reechee@localhost:5432'

SQLITE = 'sqlite:///database/database.db'


Session = sessionmaker()

# engine = create_engine(DATABASE_URI, echo=True, connect_args={'check_same_thread': False})
engine = create_engine(DATABASE_URI, echo=True)


Session.configure(bind=engine)


session = Session()
# declare a mapping 

Base = declarative_base()
# Base.metadata.create_all(engine)

#  create a schema
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,  unique=True)
    name = Column(String, nullable=False)
    language = Column(String)
    registered_date = Column(String)
    is_new_user = Column(Boolean)
    last_visted = Column(String)
    wallet_address = Column(Integer)

    account_balance = Column(Integer)
    active_investment = Column(Integer)
    pending_investment = Column(Integer)
    active_reinvestment = Column(Integer)

    transactions = relationship("Transactions", uselist=True, backref="user")


    def __init__(self, user_id, name, is_admin=False, is_new_user=True):
        self.user_id = user_id
        self.name = name
        self.is_admin = is_admin
        self.is_new_user = is_new_user
        self.registered_date = datetime.now().isoformat()

        self.account_balance = 0
        self.active_investment = 0
        self.active_reinvestment = 0
        self.pending_investment = 0
        
    def exists(self):
        return session.query(exists().where(User.user_id == self.user_id)).scalar()

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
    amount = Column(Integer)
    wallet_address = Column(String)
    date = Column(String)
    start_date = Column(String)

    balance = Column(Integer)
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
    
    def commit(self):
        session.add(self)
        session.commit()

    def start_date(self):
        return (self.start_date).isoformat().strftime("%A %d. %B %Y")
    
    def close_date(self):
        return (self.start_date + timedelta(days=180)).isoformat().strftime("%A %d. %B %Y")

    def __repr__(self):
        return f"Transaction {self.user_id} {self.transaction_type} {self.amount}"