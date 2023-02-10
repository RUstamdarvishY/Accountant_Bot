from sqlalchemy.orm import sessionmaker
from utils.db_api.models import engine, Expense
from datetime import datetime

Session = sessionmaker(bind=engine)


# def get_expense_stats_for_chat():
#     session = Session()
#     expenses = session.query(Expense)
    
#     expenses_for_one_day = sum(expenses.filter())
#     expenses_for_one_week = 
#     expenses_for_one_month = 
#     message1 = 
    
#     message2 =
    
#     message3 =
    
#     return message1+message2+message3