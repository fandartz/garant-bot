from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from functions.markup import *

from functions.disp import dp, bot

import functions.afunc as afunc

import db

class Spam(StatesGroup):
    text = State()

class aDispute_Msg(StatesGroup):
    deal_id = State()
    text = State()

#-----------------------------------КНОПКИ
@dp.message_handler(text=['⚙️ Админка'])
async def admin(message: types.Message):
    check = await db.check_admin(message.from_user.id)
    if (check == 1):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(f"✉️ Рассылка", callback_data=f"spam"))
        keyboard.add(InlineKeyboardButton(f"👤 Список админов", callback_data=f"admins"))
        keyboard.add(InlineKeyboardButton(f"📊 Статистика", callback_data=f"stat"))
        keyboard.add(InlineKeyboardButton(f"🗣 Открытые споры", callback_data=f"adisputes"))
        keyboard.add(InlineKeyboardButton(f"💸 Заявки на вывод", callback_data=f"apayouts"))
        await message.answer(f"Добро пожаловать!\nВыберите действие", reply_markup=keyboard)

@dp.callback_query_handler(text_startswith="back_to_amenu", state="*")
async def spam(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"✉️ Рассылка", callback_data=f"spam"))
    keyboard.add(InlineKeyboardButton(f"👤 Список админов", callback_data=f"admins"))
    keyboard.add(InlineKeyboardButton(f"📊 Статистика", callback_data=f"stat"))
    keyboard.add(InlineKeyboardButton(f"🗣 Открытые споры", callback_data=f"adisputes"))
    keyboard.add(InlineKeyboardButton(f"💸 Заявки на вывод", callback_data=f"apayouts"))
    await call.message.edit_text(f"Добро пожаловать!\nВыберите действие", reply_markup=keyboard)
#-----------------------------------КНОПКИ

#-----------------------------------ВЫВОД СРЕДСТВ
@dp.callback_query_handler(text_startswith="apayouts", state="*")
async def payouts(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Заявки на вывод:", reply_markup=await afunc.payouts(0))

@dp.callback_query_handler(text_startswith="payouts_open:", state="*")
async def payouts(call: types.CallbackQuery, state: FSMContext):
    id_payouts = int(call.data.split(":")[1])
    check = await db.current_payout(id_payouts)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"✅Одобрить заявку", callback_data=f"success_payouts:{id_payouts}"), InlineKeyboardButton(f"❌Удалить заявку", callback_data=f"del_payouts:{id_payouts}"))
    keyboard.add(InlineKeyboardButton(f"Назад", callback_data=f"apayouts"))
    await call.message.edit_text(f"<b>Заявка №{id_payouts}</b>\n<b>Пользователь: </b><a href='tg://user?id={check[1]}'>{check[2]}</a>\n<b>Сумма вывода:</b> {check[3]}\n<b>Куда выводить:</b> {check[5]}", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(text_startswith="success_payouts:", state="*")
async def payouts(call: types.CallbackQuery, state: FSMContext):
    id_payouts = int(call.data.split(":")[1])
    await db.upd_payout(id_payouts)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Вернуться", callback_data=f"apayouts"))
    await call.message.edit_text(f"Заявка одобрена!", reply_markup=keyboard)

@dp.callback_query_handler(text_startswith="del_payouts:", state="*")
async def payouts(call: types.CallbackQuery, state: FSMContext):
    id_payouts = int(call.data.split(":")[1])
    check = await db.current_payout(id_payouts)
    user = await db.profile(check[1])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Вернуться", callback_data=f"apayouts"))
    await db.upd_user("balance", int(user[6])+int(check[3]), int(user[1]))
    await db.del_payout(id_payouts)
    await call.message.edit_text(f"Заявка удалена!", reply_markup=keyboard)
#-----------------------------------ВЫВОД СРЕДСТВ

#-----------------------------------РАССЫЛКА
@dp.callback_query_handler(text_startswith="spam", state="*")
async def spam(call: types.CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Вернуться", callback_data=f"back_to_amenu"))
    await call.message.edit_text("Введите текст рассылки (Можно также отправить фото/видео/гс)", reply_markup=keyboard)
    await Spam.text.set()

@dp.message_handler(content_types=['any'], state=Spam.text)
async def spam(message: types.Message, state: FSMContext):
    users = await db.users()
    user = 0
    for count in range(len(users)):
        if (users[count][1] != message.from_user.id):
            try:
                await bot.copy_message(chat_id=users[count][1], from_chat_id=message.chat.id, message_id=message.message_id)
                user += 1
            except:
                pass
    await state.finish()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Вернуться", callback_data=f"back_to_amenu"))
    await message.answer(f"📬Сообщение отправлено для *{user}* пользователей!", reply_markup=keyboard, parse_mode="Markdown")
#-----------------------------------РАССЫЛКА

#-----------------------------------СПОРЫ
#Выбор спора
@dp.callback_query_handler(text_startswith="adisputes", state="*")
async def spam(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите нужный спор:", reply_markup=await afunc.adisputes(0))

#Открытие спора
@dp.callback_query_handler(text_startswith="adisp_open:", state="*")
async def spam(call: types.CallbackQuery, state: FSMContext):
    deal_id = int(call.data.split(":")[1])
    disp = await afunc.a_disp_open(deal_id, 0)
    await call.message.edit_text(disp[0], reply_markup=disp[1], parse_mode="Markdown")

#Добавление сообщений в споре
@dp.callback_query_handler(text_startswith="adisp_add_msg:", state="*")
async def disp_add_msg(call: types.CallbackQuery, state: FSMContext):
    deal_id = int(call.data.split(":")[1])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Отмена", callback_data=f"adisp_open::{deal_id}"))
    await call.message.edit_text("Введите ваше сообщение ниже:", reply_markup=keyboard)
    await aDispute_Msg.text.set()
    await state.update_data(deal_id=deal_id)

#Сообщение к спору
@dp.message_handler(state=aDispute_Msg.text)
async def disp_add_msg(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Вернуться к спору", callback_data=f"adisp_open:{int(data['deal_id'])}"))
    await db.dispute_add_msg("admin", data['text'], int(data['deal_id']))
    check = await db.deal(int(data['deal_id']))
    await bot.send_message(check[1], f"Администратор оставил сообщение в споре о сделке №{check[0]}")
    await bot.send_message(check[2], f"Администратор оставил сообщение в споре о сделке №{check[0]}")
    await message.answer("Сообщение добавлено!", reply_markup=keyboard)

#Закрытие спора в пользу юзера
@dp.callback_query_handler(text_startswith="disp_close", state="*")
async def spam(call: types.CallbackQuery, state: FSMContext):
    type = call.data.split(":")[1]
    deal_id = int(call.data.split(":")[2])
    check = await db.deal(deal_id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Вернуться к спорам", callback_data=f"adisputes"))
    if (type == "seller"):
        profile = await db.profile(check[1])
        await db.dispute_update(deal_id, check[1])
        await bot.send_message(check[1], f"Решение администрации в споре о сделке №{check[0]}: закрыто в сторону продавца")
        await bot.send_message(check[2], f"Решение администрации в споре о сделке №{check[0]}: закрыто в сторону продавца")
        await db.upd_deal(deal_id, 5)
        await db.upd_user("balance", profile[6]+(check[6]*0.95), check[1])
        await call.message.edit_text("Спор закрыт", reply_markup=keyboard)
    elif (type == "buyer"):
        await db.dispute_update(deal_id, check[2])
        await bot.send_message(check[1], f"Решение администрации в споре о сделке №{check[0]}: закрыто в сторону покупателя")
        await bot.send_message(check[2], f"Решение администрации в споре о сделке №{check[0]}: закрыто в сторону покупателя")
        await db.upd_deal(deal_id, 5)
        await db.upd_user("balance", profile[6]+(check[6]*0.95), check[2])
        await call.message.edit_text("Спор закрыт", reply_markup=keyboard)
#-----------------------------------СПОРЫ

#-----------------------------------СТАТИСТИКА
@dp.callback_query_handler(text_startswith="stat", state="*")
async def stat(call: types.CallbackQuery, state: FSMContext):
    users = await db.users()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Вернуться", callback_data=f"back_to_amenu"))
    await call.message.edit_text(f"Общее количество пользователей: {len(users)}", reply_markup=keyboard)
#-----------------------------------СТАТИСТИКА

#-----------------------------------АДМИНЫ
@dp.callback_query_handler(text_startswith="admins", state="*")
async def admins(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(f"Список админов:", reply_markup=await afunc.admins(0))

@dp.callback_query_handler(text_startswith="admin_open:", state="*")
async def admins(call: types.CallbackQuery, state: FSMContext):
    userid = int(call.data.split(":")[1])
    profile = await db.profile(userid)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Снять администратора", callback_data=f"admin:{profile[1]}"))
    keyboard.add(InlineKeyboardButton(f"Вернуться в админ меню", callback_data=f"back_to_amenu"))
    await call.message.edit_text(f"Пользователь: <a href='tg://user?id={profile[1]}'>{profile[2]}</a>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(text_startswith="admin:", state="*")
async def admin(call: types.CallbackQuery, state: FSMContext):
    userid = int(call.data.split(":")[1])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Вернуться в админ меню", callback_data=f"back_to_amenu"))
    await db.upd_user("is_admin", 0, userid)
    await db.upd_user_adm("status", "User", userid)
    await call.message.edit_text("Пользователь снят с должности администратора!", reply_markup=keyboard)
    await bot.send_message(userid, "Вас сняли с должности администратора!", reply_markup=mainMenu)
#-----------------------------------АДМИНЫ

#-----------------------------------ОБРАБОТЧИКИ
@dp.callback_query_handler(text_startswith="adm_swipe:", state="*")
async def NextOrBack(call: types.CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    await call.message.edit_text(f"Список админов:", reply_markup=await afunc.admins(remover))

@dp.callback_query_handler(text_startswith="adisp_swipe:", state="*")
async def NextOrBack(call: types.CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    await call.message.edit_text(f"Список админов:", reply_markup=await afunc.adisputes(remover))

@dp.callback_query_handler(text_startswith="adispute_swipe:", state="*")
async def NextOrBack(call: types.CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    deal_id = int(call.data.split(":")[2])
    disp = await afunc.a_disp_open(deal_id, remover)
    await call.message.edit_text(disp[0], reply_markup=disp[1], parse_mode="Markdown")
#-----------------------------------ОБРАБОТЧИКИ