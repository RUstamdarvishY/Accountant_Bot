import re

from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from utils.db_api.orm_func import add_email


class FSMEmail(StatesGroup):
    email = State()


async def fsm_start(message: types.Message):
    await FSMEmail.email.set()
    await message.reply('Если хотите отменить ввод, отправьте отмена\nВведите емейл')


async def get_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text

    email = data['email']

    pattern = re.compile(
        r'^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$')
    telegram_id = message.from_user.id

    if pattern.match(email):
        add_email(telegram_id, email)
        await message.reply('Емейл добавлен')
        await state.finish()
    else:
        await message.answer('Емейл неправильно введен')
        await state.finish()


async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ок')


def register_email_states_handlers(dp: Dispatcher):
    dp.register_message_handler(
        fsm_start, commands=['add_email'], state=None)
    dp.register_message_handler(cancel, state='*', commands=['Отмена'])
    dp.register_message_handler(cancel, Text(equals='Отмена',
                                             ignore_case=True), state='*')
    dp.register_message_handler(get_email, state=FSMEmail.email)
