from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

Base = declarative_base()


class Participant(Base):
    __tablename__ = "participants"
    pid = Column(Integer, primary_key=True)
    name = Column(String)
    matrix_address = Column(String)
    user_total = Column(Integer, default=0)
    # A relationship between the Participant and the Cuts table.
    cuts = relationship('Cuts', backref='participants', lazy=True, cascade="all, delete-orphan")


class DB_Order(Base):
    __tablename__ = "orders"
    oid = Column(Integer, primary_key=True)
    name = Column(String)
    total = Column(Integer)
    price = Column(Integer)
    tip = Column(Integer)
    timestamp = Column(DATETIME, default=now())
    cuts = relationship('Cuts', backref="orders", lazy=True, cascade="all,delete-orphan")


class Cuts(Base):
    __tablename__ = "cuts"
    cid = Column(Integer, primary_key=True)
    pid = Column(Integer, ForeignKey('participants.pid'))
    oid = Column(Integer, ForeignKey('orders.oid'))
    cut = Column(Integer)
    timestamp = Column(DATETIME, default=now())


def setup_db():
    db = create_engine("sqlite:///../sql/orderbot.db")
    Participant.__table__.create(bind=db, checkfirst=True)
    DB_Order.__table__.create(bind=db, checkfirst=True)
    Cuts.__table__.create(bind=db, checkfirst=True)