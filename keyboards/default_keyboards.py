from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button1 = KeyboardButton('/Добавит_емейл')
button2 = KeyboardButton('/Добавить_расход')
button3 = KeyboardButton('/Отправить_статистику')
button4 = KeyboardButton('/Показать_категории_расходов')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(button1).insert(button2).add(button3).insert(button4)


button1 = KeyboardButton('$')
button2 = KeyboardButton('€')
button3 = KeyboardButton('₽')
button4 = KeyboardButton('бел. рубли')

currency_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

currency_kb.add(button1).insert(button2).insert(button3).add(button4)


