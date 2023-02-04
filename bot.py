import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from decouple import config

bot = Bot(token=config('BOT_TOKEN'))
dp = Dispatcher(bot)


async def on_startup(_):
    print('bot is online')


async def on_shutdown(_):
    print('bot is offline')

executor.start_polling(dp, skip_updates=True)
