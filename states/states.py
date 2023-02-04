import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config


storage = MemoryStorage()
bot = Bot(token=config('BOT_TOKEN'))
dp = Dispatcher(bot, storage=storage)


class FSMAdmin(StatesGroup):
    price = State()
    category = State()


@dp.message_handler(commands=['Добавить_расход'], state=None)
async def fsm_start(message: types.Message):
    await FSMAdmin.price.set()
    await message.reply('Введите цену')


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Отмена')


@dp.message_handler(content_types=['text'], state=FSMAdmin.price)
async def get_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await FSMAdmin.next()
    await message.reply('Введите категорию расходов')


@dp.message_handler(content_types=['text'], state=FSMAdmin.name)
async def get_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await message.reply('Данные занесены в базу')
    await state.finish()


