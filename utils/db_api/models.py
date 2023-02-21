from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from decouple import config


DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')
connection_string = f'postgresql://{DB_USER}:{DB_PASS}@localhost/bot_base'


engine = create_engine(connection_string)

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    telegram_id = Column(Integer, nullable=False)
    email = Column(String(255), nullable=True)
    expenses = relationship('Expense', backref='user')


class Expense(Base):
    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    expenses = relationship('Expense', backref='category')



Base.metadata.create_all(engine)
