from pathlib import Path

from aiogram import types
from aiogram.dispatcher import Dispatcher

from sqlalchemy.orm import sessionmaker

from create_bot import bot
from keyboards import kb_client, inline_kb_client
from utils.db_api.models import engine, User, Category, Expense
from utils.db_api.orm_func import get_expense_stats_for_chat
from utils.misc import rate_limit
from utils.misc.plots import save_plots
from utils.misc.mail import send_email


Session = sessionmaker(bind=engine)


@rate_limit(limit=7, key='/start')
async def commands_start(message: types.Message):
    telegram_id = message.from_user.id
    username = message.from_user.username

    session = Session()
    user_id = session.query(User).filter(
        User.telegram_id == telegram_id).first()

    if user_id == None:
        user = User(username=username, telegram_id=telegram_id)
        session.add(user)
        session.commit()

    await message.answer('Что вы хотите сделать', reply_markup=kb_client)


@rate_limit(limit=7, key='/help')
async def commands_help(message: types.Message):
    await bot.send_message(message.from_user.id, 'Этот бот может вести учет ваших расходов и высылать статистику в чат или более подробную статистику на емейл, введите комманду /start')


@rate_limit(limit=7, key='/send_statistics')
async def send_statistics(message: types.Message):
    session = Session()
    if session.query(Expense).count() > 0:
        await message.answer('Отправить', reply_markup=inline_kb_client)
    else:
        await message.answer('Нет расходов')


async def statistics_callback(callback: types.CallbackQuery):
    telegram_id = callback.from_user.id

    if callback.data == 'email':
        plot = Path('graphs.pdf').absolute()
        if plot.is_file():
            plot.unlink()
        save_plots(f'graphs.pdf')

        session = Session()
        user_email = session.query(User.email).filter(
            User.telegram_id == telegram_id).first()

        if user_email:
            send_email(user_email[0])
        else:
            await callback.message.answer('Не указан емейл')

        await callback.message.answer('Статистика отправлена на емейл')
    else:
        await callback.message.answer(get_expense_stats_for_chat(1) + get_expense_stats_for_chat(7) + get_expense_stats_for_chat(30))


@rate_limit(limit=7, key='/send_expenses_categories')
async def list_expenses_categories(message: types.Message):
    msg = ''
    session = Session()
    categories = session.query(Category)

    for index, category in enumerate(categories):
        msg += f'категория №{index+1}: {category.title}\n'
        
    if msg:
        await message.reply(msg)
    else: 
        await message.reply('Нет категорий')


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(
        commands_start, commands=['start'])
    dp.register_message_handler(
        commands_help, commands=['help'])
    dp.register_message_handler(
        send_statistics, commands=['send_statistics'])
    dp.register_message_handler(
        list_expenses_categories, commands=['send_expenses_categories'])
    dp.register_callback_query_handler(statistics_callback)
