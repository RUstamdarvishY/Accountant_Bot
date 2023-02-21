from aiogram.utils import executor

from create_bot import dp, bot
from handlers import user_handlers
from states import expenses_states, email_states

from decouple import config


async def on_startup(dp):
    import middlewares
    middlewares.setup(dp)
    await bot.set_webhook(config('APP_URL'))
    print('bot is online')


user_handlers.register_user_handlers(dp)
expenses_states.register_expense_states_handlers(dp)
email_states.register_email_states_handlers(dp)


async def on_shutdown(dp):
    await bot.delete_webhook(config('APP_URL'))

executor.start_webhook(
    dispatcher=dp,
    webhook_path='',
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host="0.0.0.0",
    port=config('PORT', default=5000))
