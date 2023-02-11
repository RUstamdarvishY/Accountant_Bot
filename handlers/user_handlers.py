import logging
import re

from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from sqlalchemy.orm import sessionmaker

from create_bot import dp, bot
from keyboards import kb_client, inline_kb_client
from utils.db_api.models import engine, User, Category
from utils.db_api.orm_func import get_expense_stats_for_chat 



Session = sessionmaker(bind=engine)


async def set_all_default_commands(bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('start', 'начало работы'),
            BotCommand('help', 'описание бота'),
            BotCommand('Добавить_емейл',
                       'добавить емейл по которому будет отправляться статистика'),
            BotCommand('Отправить статистику',
                       'отправляет статистику в чат или на емейл'),
            BotCommand('Показать_категории_расходов',
                       'показывает существующие категории расходов'),
            BotCommand('Добавить_расход',
                       'Добавляет расход в существующую или новую категорию'),
        ],
        scope=BotCommandScopeDefault()
    )


# @dp.message_handler(commands=['start'])
async def commands_start(message: types.Message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    
    session = Session()
    user = User(username=username, telegram_id=telegram_id)
    session.add(user)
    session.commit()
    
    await message.answer('Что вы хотите сделать', reply_markup=kb_client)
    await set_all_default_commands(message.bot, message.from_user.id)


# @dp.message_handler(commands=['help'])
async def commands_help(message: types.Message):
    await bot.send_message(message.from_user.id, 'Этот бот может вести учет ваших расходов и высылать статистику в чат или более подробную статистику на емейл, введите комманду /start')
    await set_all_default_commands(message.bot, message.from_user.id)


# @dp.message_handler(commands=['Добавить_емейл'])
async def commands_add_email(message: types.Message):
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
    await set_all_default_commands(message.bot, message.from_user.id)
    


# @dp.message_handler(commands=['Отправить_статистику'])
async def commands_send_statistics(message: types.Message):
    await message.answer('Отправить', reply_markup=inline_kb_client)
    await set_all_default_commands(message.bot, message.from_user.id)
    


# @dp.callback_query_handler(text='email')
async def send_to_email(callback: types.CallbackQuery):
    await callback.message.answer('Статистика отправлена на емейл')
    await callback.answer()


# @dp.callback_query_handler(text='chat')
async def send_to_chat(callback: types.CallbackQuery):
    await callback.message.answer(get_expense_stats_for_chat())
    await callback.answer()


# @dp.message_handler(commands=['Показать_категории_расходов'])
async def commands_list_expenses_categories(message: types.Message):
    message = ''
    session = Session()
    categories = session.query(Category)

    for index, category in enumerate(categories):
        message += f'category №{index}: {category.title}\n'
        
        
    await message.answer(message)
    await set_all_default_commands(message.bot, message.from_user.id)
    


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(
        commands_start, commands=['start'])
    dp.register_message_handler(
        commands_help, commands=['help'])
    dp.register_message_handler(
        commands_add_email, commands=['Добавить_емейл'])
    dp.register_message_handler(
        commands_send_statistics, commands=['Отправить_статистику'])
    dp.register_message_handler(
        commands_list_expenses_categories, commands=['Показать_категории_расходов'])
    dp.register_callback_query_handler(send_to_email, callback='email')
    dp.register_callback_query_handler(send_to_chat, callback='chat')
