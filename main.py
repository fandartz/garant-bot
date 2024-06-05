from functions.markup import AmainMenu, mainMenu

from handlers.handlers import *
from handlers.adm_handlers import *

from functions.disp import dp, bot

from aiogram import types

from aiogram.utils import executor

import db as db

always_admin=1111

async def on_startup(_):
	await db.db_start()
	print('Бот запущен')

#Запуск бота
@dp.message_handler(commands=['start'])
async def bot_message(message: types.Message):
	if (message.from_user.id == always_admin):
		is_admin = 1
		await db.cmd_start_db(message.from_user.id, message.from_user.full_name, message.from_user.username, is_admin, "Admin")
	else:
		is_admin = 0
		await db.cmd_start_db(message.from_user.id, message.from_user.full_name, message.from_user.username, is_admin, "User")
	check = await db.check_admin(message.from_user.id)

	if (check == 1):
		await bot.send_message(message.from_user.id, "<b>Добро пожаловать!</b>\n\n"
						"<b>Бот предназначен</b> для проведения безопасных сделок.\n\n"
						"<b>Как это устроено?</b>"
						"\n● Автогарант - это доп. звено в сделке через которое проходят услуги и деньги таким образом, чтобы обеспечить безопасность обоих участников."
						"\n\n<b>Сервис взимает комиссию в 5%</b>"
						"\n[И комиссия от платежных систем]"
						"\n\n<b>🎖Статистика:</b>"
						#"\n├ Сервису более <b>3-х лет</b>"
						f"\n├ Пользователей: <b>{len(await db.users())}</b>"
						f"\n├ Проведено сделок: <b>{len(await db.deals())}</b>"
						f"\n└ На сумму: <b>{await db.deals_sum()} ₽</b>"
						"\n\n<a href='https://google.com'>📃Инструкция</a> |  <a href='https://google.com'>📁Правила</a> "
						"\n<a href='https://google.com'>⚡️Проекты</a>       |  <a href='https://google.com'>💬Отзывы</a>", reply_markup=AmainMenu, parse_mode='HTML')
	else:
		await bot.send_message(message.from_user.id, "<b>Добро пожаловать!</b>\n\n"
						"<b>Бот предназначен</b> для проведения безопасных сделок.\n\n"
						"<b>Как это устроено?</b>"
						"\n● Автогарант - это доп. звено в сделке через которое проходят услуги и деньги таким образом, чтобы обеспечить безопасность обоих участников."
						"\n\n<b>Сервис взимает комиссию в 5%</b>"
						"\n[И комиссия от платежных систем]"
						"\n\n<b>🎖Статистика:</b>"
						#"\n├ Сервису более <b>3-х лет</b>"
						f"\n├ Пользователей: <b>{len(await db.users())}</b>"
						f"\n├ Проведено сделок: <b>{len(await db.deals())}</b>"
						f"\n└ На сумму: <b>{await db.deals_sum()} ₽</b>"
						"\n\n<a href='https://google.com'>📃Инструкция</a> |  <a href='https://google.com'>📁Правила</a> "
						"\n<a href='https://google.com'>⚡️Проекты</a>       |  <a href='https://google.com'>💬Отзывы</a>", reply_markup=mainMenu, parse_mode='HTML')
	



if __name__ == '__main__':
	executor.start_polling(dp, on_startup=on_startup, skip_updates=True, allowed_updates=types.AllowedUpdates.all())