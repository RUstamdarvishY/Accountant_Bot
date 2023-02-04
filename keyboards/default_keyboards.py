import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from decouple import config


bot = Bot(token=config('BOT_TOKEN'))
dp = Dispatcher(bot)

button1 = KeyboardButton('/Добавит_емейл')
button2 = KeyboardButton('/Добавить_расход')
button3 = KeyboardButton('/Отправить_статистику')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(button1).add(button2).insert(button3)


@dp.message_handler(commands=['start'])
async def reply(message: types.Message):
    await message.answer('Что вы хотите сделать', reply_markup=kb_client)   

@dp.message_handler()
async def reply(message: types.Message):
    await message.answer('Хорошо', reply_markup=ReplyKeyboardRemove)
