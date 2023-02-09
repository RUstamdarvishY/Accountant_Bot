from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from decouple import config


bot = Bot(token=config('BOT_TOKEN'))
dp = Dispatcher(bot)
