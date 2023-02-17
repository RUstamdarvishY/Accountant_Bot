from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from decouple import config


storage = MemoryStorage()

bot = Bot(token=config('BOT_TOKEN'))
dp = Dispatcher(bot, storage=storage)
