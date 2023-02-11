import logging

from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from sqlalchemy.orm import sessionmaker

from handlers.user_handlers import set_all_default_commands
from utils.db_api.models import engine, Expense, Category
from create_bot import dp
from keyboards import currency_kb


storage = MemoryStorage()
Session = sessionmaker(bind=engine)

class FSMExpense(StatesGroup):
    price = State()
    currency = State()
    category = State()


# @dp.message_handler(commands=['Добавить_расход'], state=None)
async def fsm_start(message: types.Message):
    await FSMExpense.price.set()
    await message.reply('Введите цену')
    await set_all_default_commands(message.bot, message.from_user.id)


# @dp.message_handler(content_types=['text'], state=FSMExpense.price)
async def get_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await FSMExpense.next()
    await message.reply('Введите валюту', reply_markup=currency_kb)


# @dp.message_handler(content_types=['text'], state=FSMExpense.currency)
async def get_currency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['currency'] = message.text
    await FSMExpense.next()
    await message.reply('Введите категорию расходов')


# @dp.message_handler(content_types=['text'], state=FSMExpense.category)
async def get_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
        
    user_id = message.from_user.id
    
    session = Session()
    price = data['price']
    currency = data['currency']
    category = data['category']
    
    category_id = session.query(Category).filter(Category.title == category).first()
    
    if not category_id.exists():
        new_category = Category(title=category)
        category_id = new_category.id
        session.add(new_category)
            
    expense = Expense(price, currency, category_id=category_id, user_id=user_id)
        
    session.add(expense)
    session.commit()
    
    await message.reply('Данные занесены в базу')
    await state.finish()


# @dp.message_handler(state='*', commands=['Отмена'])
# @dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ок')


def register_states_handlers(dp: Dispatcher):
    dp.register_message_handler(
        fsm_start, commands=['Добавить_расход'], state=None)
    dp.register_message_handler(cancel, state='*', commands=['Отмена'])
    dp.register_message_handler(cancel, Text(equals='Отмена',
                                             ignore_case=True), state='*')
    dp.register_message_handler(get_price, state=FSMExpense.price)
    dp.register_message_handler(get_currency, state=FSMExpense.currency)
    dp.register_message_handler(get_category, state=FSMExpense.category)
