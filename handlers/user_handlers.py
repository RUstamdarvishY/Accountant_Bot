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


async def add_email(message: types.Message):
    message.reply('Введите емейл')
    pattern = re.compile(r'[\w.-]+@[\w.]\.(com|ru|by)')

    if not pattern.match(message.text):
        await message.answer('Емейл неправильно введен')

    user_id = message.from_user.id

    session = Session()
    user = session.query(User).filter(user_id == user_id).first()
    user.email = message.text
    session.commit()

    await message.answer('Емейл добавлен')


async def send_statistics(message: types.Message):
    await message.answer('Отправить', reply_markup=inline_kb_client)


async def send_to_email(callback: types.CallbackQuery):
    await callback.message.answer('Статистика отправлена на емейл')
    await callback.answer()


async def send_to_chat(callback: types.CallbackQuery):
    await callback.message.answer(get_expense_stats_for_chat())
    await callback.answer()


async def list_expenses_categories(message: types.Message):
    message = ''
    session = Session()
    categories = session.query(Category)

    for index, category in enumerate(categories):
        message += f'category №{index}: {category.title}\n'

    await message.answer(message)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(
        commands_start, commands=['start'])
    dp.register_message_handler(
        commands_help, commands=['help'])
    dp.register_message_handler(
        add_email, commands=['Добавить_емейл'])
    dp.register_message_handler(
        send_statistics, commands=['Отправить_статистику'])
    dp.register_message_handler(
        list_expenses_categories, commands=['Показать_категории_расходов'])
    dp.register_callback_query_handler(send_to_email)
    dp.register_callback_query_handler(send_to_chat)
