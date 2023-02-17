from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils.db_api.orm_func import send_expense_to_database
from utils.misc import rate_limit
from keyboards import currency_kb, kb_client


class FSMExpense(StatesGroup):
    price = State()
    currency = State()
    category = State()


@rate_limit(limit=7, key='/add_expense')
async def fsm_start(message: types.Message):
    await FSMExpense.price.set()
    await message.reply('Если хотите отменить ввод, отправьте отмена\nВведите цену')


async def get_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    if message.text.isdigit():
        await FSMExpense.next()
        await message.reply('Введите валюту', reply_markup=currency_kb)
    else:
        await message.reply('Введено не число')
        await state.finish()


async def get_currency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['currency'] = message.text
    await FSMExpense.next()
    await message.reply('Введите категорию расходов', reply_markup=ReplyKeyboardRemove())


async def get_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    telegram_id = message.from_user.id
    price = data['price']
    currency = data['currency']
    category = data['category']

    send_expense_to_database(price, currency, category, telegram_id)

    await message.reply('Данные занесены в базу', reply_markup=kb_client)
    await state.finish()


async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ок', reply_markup=kb_client)


def register_expense_states_handlers(dp: Dispatcher):
    dp.register_message_handler(
        fsm_start, commands=['add_expense'], state=None)
    dp.register_message_handler(cancel, state='*', commands=['Отмена'])
    dp.register_message_handler(cancel, Text(equals='Отмена',
                                             ignore_case=True), state='*')
    dp.register_message_handler(get_price, state=FSMExpense.price)
    dp.register_message_handler(get_currency, state=FSMExpense.currency)
    dp.register_message_handler(get_category, state=FSMExpense.category)
