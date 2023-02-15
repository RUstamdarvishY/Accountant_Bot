import logging
from aiogram import types
from aiogram.utils import executor
from create_bot import dp, bot
from handlers import user_handlers
from states import expenses_states
from handlers.setting_comands import set_all_default_commands


async def on_startup(_):
    print('bot is online')


async def commands_menu(bot: bot):
    await set_all_default_commands(bot)


user_handlers.register_user_handlers(dp)
expenses_states.register_states_handlers(dp)


async def on_shutdown(_):
    print('bot is offline')

executor.start_polling(dp, skip_updates=True,
                       on_startup=on_startup, on_shutdown=on_shutdown)
