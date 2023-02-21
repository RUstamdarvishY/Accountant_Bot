from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button1 = KeyboardButton('/add_email')
button2 = KeyboardButton('/add_expense')
button3 = KeyboardButton('/send_statistics')
button4 = KeyboardButton('/send_expenses_categories')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(button1).insert(button2).add(button3).insert(button4)
