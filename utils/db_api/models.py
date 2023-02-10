from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


engine = create_engine('postgresql://postgres:{PASSWORD}@{PORT}/{DATABASE_NAME}')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users' 
    
    user_id = Column(Integer, primary_key=True) 
    username = Column(String(255), nullable=False) 
    telegram_id = Column(Integer, nullable=False)
    email = Column()
    expenses = relationship("Expense", back_populates="users")
    
    
class Expense(Base):
    __tablename__ = 'expenses'
    
    expense_id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    categories = relationship("Category", back_populates="expenses")
    user_id = Column(Integer, ForeignKey("user.id")) 
    users = relationship("User", back_populates="expenses")
    
class Category(Base):
    __tablename__ = 'categories'
    
    category_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    expenses = relationship("Expense", back_populates="categories")
     
    
# Base.metadata.create_all(engine)