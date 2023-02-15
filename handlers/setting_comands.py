from aiogram.types import BotCommand, BotCommandScopeDefault
from create_bot import bot


async def set_all_default_commands(bot: bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('start', 'начало работы'),
            BotCommand('help', 'описание бота'),
            BotCommand('Добавить_емейл',
                       'добавить емейл по которому будет отправляться статистика'),
            BotCommand('Отправить статистику',
                       'отправляет статистику в чат или на емейл'),
            BotCommand('Показать_категории_расходов',
                       'показывает существующие категории расходов'),
            BotCommand('Добавить_расход',
                       'Добавляет расход в существующую или новую категорию'),
        ],
        scope=BotCommandScopeDefault()
    )
