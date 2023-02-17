from aiogram.utils import executor

from create_bot import dp
from handlers import user_handlers
from states import expenses_states, email_states



async def on_startup(_):
    import middlewares
    middlewares.setup(dp)
    print('bot is online')


user_handlers.register_user_handlers(dp)
expenses_states.register_expense_states_handlers(dp)
email_states.register_email_states_handlers(dp)


async def on_shutdown(_):
    print('bot is offline')

executor.start_polling(dp, skip_updates=True,
                       on_startup=on_startup, on_shutdown=on_shutdown)
