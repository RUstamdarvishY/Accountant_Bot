from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker

from utils.db_api.models import engine, Expense, Category, User


Session = sessionmaker(bind=engine)

# фильрует расходы по отрезкам времени (день, неделя, месяц), а также возвращает категорию с самыми большими расходами за данный промежуток времени


def get_expense_stats_for_chat() -> str:
    session = Session()
    expenses = session.query(Expense)

    expenses_for_one_day = sum(expenses.filter(
        Expense.time > datetime.now() - timedelta(days=1),
        Expense.time < datetime.now()).only(Expense.price))

    category_id1 = session.query(Expense).\
        filter(Expense.time > datetime.now() - timedelta(days=1),
               Expense.time < datetime.now()).\
        order_by(Expense.price).limit(1).only(Expense.category_id)

    category_with_most_expenses_day = session.query(
        Category).filter(Category.id == category_id1).only(Category.title)

    expenses_for_one_week = sum(expenses.filter(
        Expense.time > datetime.now() - timedelta(days=7),
        Expense.time < datetime.now()).only(Expense.price))

    category_id2 = session.query(Expense).\
        filter(Expense.time > datetime.now() - timedelta(days=7),
               Expense.time < datetime.now()).\
        order_by(Expense.price).limit(1).only(Expense.category_id)

    category_with_most_expenses_week = session.query(Category).filter(
        Category.id == category_id2).only(Category.title)

    expenses_for_one_month = sum(expenses.filter(
        Expense.time > datetime.now() - timedelta(days=30),
        Expense.time < datetime.now()).only(Expense.price))

    category_id3 = session.query(Expense).\
        filter(Expense.time > datetime.now() - timedelta(days=30),
               Expense.time < datetime.now()).\
        order_by(Expense.price).limit(1).only(Expense.category_id)

    category_with_most_expenses_month = session.query(Category).filter(
        Category.id == category_id3).only(Category.title)

    message1 = f'за последние 24 часа вы потратили {expenses_for_one_day}, категория с наибольшими расходами - {category_with_most_expenses_day}\n'

    message2 = f'за последнюю неделю вы потратили {expenses_for_one_week}, категория с наибольшими расходами - {category_with_most_expenses_week}\n'

    message3 = f'за последний месяц вы потратили {expenses_for_one_month}, категория с наибольшими расходами - {category_with_most_expenses_month}'

    return message1 + message2 + message3


def send_expense_to_database(price, currency, category, telegram_id):
    session = Session()

    find_category = session.query(Category).filter(
        Category.title == category).first()

    user = session.query(User).filter(
        User.telegram_id == telegram_id).first()

    if find_category == None:
        new_category = Category(title=category)
        session.add(new_category)
        session.commit()
        find_category = new_category

    expense = Expense(
        time=datetime.now(), price=price, currency=currency,
        category_id=find_category.id, user_id=user.id)

    session.add(expense)
    session.commit()


def add_email(telegram_id, email):
    session = Session()
    user = session.query(User).filter(telegram_id == telegram_id).first()        
    user.email = email
    session.commit()