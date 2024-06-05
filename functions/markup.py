from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

btn1 = KeyboardButton('🔍 Найти user')
btn3 = KeyboardButton('🎩 Мой профиль')
btn4 = KeyboardButton('💬 Помощь')
btn5 = KeyboardButton('⚙️ Админка')
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btn1, btn3, btn4)
AmainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btn1, btn3, btn4, btn5)