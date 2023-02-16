import logging
import re

from aiogram import types
from aiogram.dispatcher import Dispatcher

from sqlalchemy.orm import sessionmaker

from create_bot import bot
from keyboards import kb_client, inline_kb_client
from utils.db_api.models import engine, User, Category
from utils.db_api.orm_func import get_expense_stats_for_chat


Session = sessionmaker(bind=engine)


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


async def commands_help(message: types.Message):
    await bot.send_message(message.from_user.id, 'Этот бот может вести учет ваших расходов и высылать статистику в чат или более подробную статистику на емейл, введите комманду /start')


async def send_statistics(message: types.Message):
    await message.answer('Отправить', reply_markup=inline_kb_client)


async def statistics_callback(callback: types.CallbackQuery):
    if callback.data == 'email':
        await callback.message.answer('Статистика отправлена на емейл')
    else:
        await callback.message.answer(get_expense_stats_for_chat())



async def list_expenses_categories(message: types.Message):
    msg = ''
    session = Session()
    categories = session.query(Category)

    for index, category in enumerate(categories):
        msg += f'категория №{index+1}: {category.title}\n'

    await message.reply(msg)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(
        commands_start, commands=['start'])
    dp.register_message_handler(
        commands_help, commands=['help'])
    dp.register_message_handler(
        send_statistics, commands=['Отправить_статистику'])
    dp.register_message_handler(
        list_expenses_categories, commands=['Показать_категории_расходов'])
    dp.register_callback_query_handler(statistics_callback)
