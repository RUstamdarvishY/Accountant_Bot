from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from decouple import config


engine = create_engine(
    'mysql+mysqlconnector://root:root@localhost/mysql', echo=True)


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, nullable=False)
    telegram_id = Column(Integer)
    username = Column(String(255))

    expense = relationship("Expense", back_populates="user", cascade="all, delete",
                           passive_deletes=True)

    category = relationship("Category", back_populates="user", cascade="all, delete",
                            passive_deletes=True)


class Expense(Base):
    __tablename__ = 'expense'

    expense_id = Column(Integer, primary_key=True, nullable=False)
    currency = Column(String(2))
    expense = Column(Integer)
    date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))
    category_id = Column(Integer, ForeignKey(
        'category.category_id', ondelete='SET NULL'))

    user = relationship("User", back_populates="expense", cascade="all, delete",
                        passive_deletes=True)

    category = relationship("Category", back_populates="expense")


class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255))
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))

    expense = relationship("Expense", back_populates="category")

    user = relationship("User", back_populates="category", cascade="all, delete",
                        passive_deletes=True)
