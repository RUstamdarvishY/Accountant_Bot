import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from decouple import config

bot = Bot(token=config('BOT_TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler(commands=['help']) 
async def commands_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Этот бот может вести учет ваших расходов и высылать статистику в чат или более подробную статистику на емейл')


@dp.message_handler(commands=['Добавить_емейл']) 
async def commands_start(message: types.Message):
    pass

@dp.message_handler(commands=['Отправить_статистику']) 
async def commands_start(message: types.Message):
    pass