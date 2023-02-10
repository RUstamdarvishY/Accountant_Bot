from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button1 = KeyboardButton('/Добавит_емейл')
button2 = KeyboardButton('/Добавить_расход')
button3 = KeyboardButton('/Отправить_статистику')
button4 = KeyboardButton('/Показать_категории_расходов')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(button1).add(button2).insert(button3).add(button4)
