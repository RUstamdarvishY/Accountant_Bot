from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker

from utils.db_api.models import engine, Expense, Category, User


Session = sessionmaker(bind=engine)

# фильрует расходы по отрезкам времени (день, неделя, месяц), а также возвращает категорию с самыми большими расходами за данный промежуток времени


def get_expense_stats_for_chat() -> str:
    session = Session()
    expenses = session.query(Expense.price)

    time_filter_day = expenses.filter(
        Expense.time > datetime.now() - timedelta(days=1),
        Expense.time < datetime.now())

    expenses_for_one_day = sum([i[0] for i in time_filter_day])

    if expenses_for_one_day > 0:
        category_filter_day = session.query(Expense.category_id).\
            filter(Expense.time > datetime.now() - timedelta(days=1),
                   Expense.time < datetime.now()).\
            order_by(Expense.price)

        category_with_most_expenses_day = session.query(
            Category.title).filter(Category.id == category_filter_day[0][0])

        message1 = f'за последние 24 часа вы потратили {expenses_for_one_day}, категория с наибольшими расходами - {category_with_most_expenses_day[0][0]}\n'
    else:
        message1 = 'за последние 24 вы ничего не потратили\n'

    time_filter_week = expenses.filter(
        Expense.time > datetime.now() - timedelta(days=7),
        Expense.time < datetime.now())

    expenses_for_one_week = sum([i[0] for i in time_filter_week])

    if expenses_for_one_week > 0:
        category_filter_week = session.query(Expense.category_id).\
            filter(Expense.time > datetime.now() - timedelta(days=7),
                   Expense.time < datetime.now()).\
            order_by(Expense.price)

        category_with_most_expenses_week = session.query(
            Category.title).filter(Category.id == category_filter_week[0][0])

        message2 = f'за последнюю неделю вы потратили {expenses_for_one_week}, категория с наибольшими расходами - {category_with_most_expenses_week[0][0]}\n'
    else:
        message2 = 'за последнюю неделю вы ничего не потратили\n'

    time_filter_month = expenses.filter(
        Expense.time > datetime.now() - timedelta(days=30),
        Expense.time < datetime.now())

    expenses_for_one_month = sum([i[0] for i in time_filter_month])

    if expenses_for_one_month > 0:
        category_filter_month = session.query(Expense.category_id).\
            filter(Expense.time > datetime.now() - timedelta(days=30),
                   Expense.time < datetime.now()).\
            order_by(Expense.price)

        category_with_most_expenses_month = session.query(
            Category.title).filter(Category.id == category_filter_month[0][0])

        message3 = f'за последний месяц вы потратили {expenses_for_one_month}, категория с наибольшими расходами - {category_with_most_expenses_month[0][0]}'
    else:
        message3 = 'за последний месяц вы ничего не потратили'

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


def list_categories():
    session = Session()
    categories = session.query(Category.title)

    return categories


def list_expenses():
    session = Session()
    expenses = session.query(Expense.price, Expense.time)

    return expenses
