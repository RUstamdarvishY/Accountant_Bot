from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_kb_client = InlineKeyboardMarkup(row_width=2)

button1 = InlineKeyboardButton(text='на емейл', callback_data='email')
button2 = InlineKeyboardButton(text='в чат', callback_data='chat')

inline_kb_client.add(button1, button2)
