from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
# from decouple import config

# bot = Bot(token=config('BOT_TOKEN'))
bot = Bot(token='5712273630:AAFVZ6h0sTODwbaw0FNWa0bQPS2i5hDxFBU')
dp = Dispatcher(bot)

@dp.message_handler() 
async def echo(message: types.Message):
    await message.answer(message.text) 
    await message.reply(message.text) 

executor.start_polling(dp, skip_updates=True) 
