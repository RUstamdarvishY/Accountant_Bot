from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker

from utils.db_api.models import engine, Expense, Category, User


Session = sessionmaker(bind=engine)

# фильрует расходы по отрезкам времени (день, неделя, месяц), а также возвращает категорию с самыми большими расходами за данный промежуток времени


def get_expense_stats_for_chat(timeframe: int) -> str:
    session = Session()
    expenses = session.query(Expense.price)
    timeframe_message = ''

    if timeframe == 1:
        timeframe_message = 'последний день'
    elif timeframe == 7:
        timeframe_message = 'последнюю неделю'
    elif timeframe == 30:
        timeframe_message = 'последний месяц'

    time_filter = expenses.filter(
        Expense.time > datetime.now() - timedelta(days=timeframe),
        Expense.time < datetime.now())

    expenses_for_timeframe = sum([i[0] for i in time_filter])

    if expenses_for_timeframe > 0:
        category_filter = session.query(Expense.category_id).\
            filter(Expense.time > datetime.now() - timedelta(days=timeframe),
                   Expense.time < datetime.now()).\
            order_by(Expense.price)

        category_with_most_expenses = session.query(
            Category.title).filter(Category.id == category_filter[0][0])

        message = f'за {timeframe_message} вы потратили {expenses_for_timeframe}, категория с наибольшими расходами - {category_with_most_expenses[0][0]}\n'
    else:
        message = f'за {timeframe_message} вы ничего не потратили\n'

    return message


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


def list_categories():
    session = Session()
    categories = session.query(Category.title)

    return categories


def list_expenses():
    session = Session()
    expenses = session.query(Expense.price, Expense.time)

    return expenses
