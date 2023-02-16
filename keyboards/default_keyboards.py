from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button1 = KeyboardButton('/add_email')
button2 = KeyboardButton('/add_expense')
button3 = KeyboardButton('/send_statistics')
button4 = KeyboardButton('/send_expenses_categories')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(button1).insert(button2).add(button3).insert(button4)


button1 = KeyboardButton('$')
button2 = KeyboardButton('€')
button3 = KeyboardButton('₽')
button4 = KeyboardButton('бел. рубли')

currency_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

currency_kb.add(button1).insert(button2).insert(button3).add(button4)


