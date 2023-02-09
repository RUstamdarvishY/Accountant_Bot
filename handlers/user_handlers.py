import logging
from aiogram import types
from aiogram.dispatcher import Dispatcher
from create_bot import dp, bot
from keyboards import kb_client


# @dp.message_handler(commands=['start'])
async def commands_start(message: types.Message):
    await message.answer('Что вы хотите сделать', reply_markup=kb_client)


# @dp.message_handler(commands=['help'])
async def commands_help(message: types.Message):
    await bot.send_message(message.from_user.id, 'Этот бот может вести учет ваших расходов и высылать статистику в чат или более подробную статистику на емейл')


# @dp.message_handler(commands=['Добавить_емейл'])
async def commands_add_email(message: types.Message):
    pass


# @dp.message_handler(commands=['Отправить_статистику'])
async def commands_send_statistics(message: types.Message):
    pass


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(
        commands_start, commands=['start'])
    dp.register_message_handler(
        commands_help, commands=['help'])
    dp.register_message_handler(
        commands_add_email, commands=['Добавить_емейл'])
    dp.register_message_handler(
        commands_send_statistics, commands=['Отправить_статистику'])
