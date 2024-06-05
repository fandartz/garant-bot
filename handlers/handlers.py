from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentTypes
from functions.markup import *

from functions.disp import dp, bot, PAYMENTS_TOKEN

from datetime import datetime as dt

import functions.func as func

import db

class FindUser(StatesGroup):
    type = State()
    find = State()

class FeedBack_add(StatesGroup):
    seller_userid = State()
    buyer_userid = State()
    type = State()
    text = State()

class DealCreate(StatesGroup):
    i_am = State()
    seller_userid = State()
    buyer_userid = State()
    seller_name = State()
    buyer_name = State()
    sum = State()
    desc = State()

class DealSend(StatesGroup):
    seller_userid = State()
    buyer_userid = State()
    deal_id = State()
    send = State()

class Dispute_Add(StatesGroup):
    from_user = State()
    seller_userid = State()
    buyer_userid = State()
    seller_name = State()
    buyer_name = State()
    deal_id = State()
    desc = State()

class Dispute_Msg(StatesGroup):
    deal_id = State()
    text = State()

class Payout_create(StatesGroup):
    text = State()
    sum = State()
    
class Donate_create(StatesGroup):
    sum = State()

class PAY(StatesGroup):
    sum = State()


#------------------------------------КНОПКИ
@dp.message_handler(text=['🎩 Мой профиль'])
async def profile(message: types.Message):
    profile = await db.profile(message.from_user.id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"🤝 Мои сделки", callback_data=f"mydeals:{message.from_user.id}"))
    keyboard.add(InlineKeyboardButton(f"🎁 Донаты", callback_data=f"donate:{message.from_user.id}"), InlineKeyboardButton(f"🗣 Споры", callback_data=f"my_disputes:{message.from_user.id}"))
    keyboard.add(InlineKeyboardButton(f"⬇️ Пополнить", callback_data=f"pays:{message.from_user.id}"), InlineKeyboardButton(f"⬆️ Вывести", callback_data=f"my_payouts:{message.from_user.id}"))
    feedbacks = await db.feedbacks(message.from_user.id)
    disputes = await db.disputes_count(message.from_user.id)
    disputes_win = await db.disputes_win(message.from_user.id)
    positive = 0
    negative = 0
    if (len(feedbacks) != 0):
        for i in range(len(feedbacks)):
            if (feedbacks[i][3] == "👍"):
                positive += 1
            elif (feedbacks[i][3] == "👎"):
                negative += 1
    await message.answer("<blockquote>👤</blockquote>\n"
                    f"<b>Пользователь:</b> @{profile[3]}\n"
                    f"<b>ID:</b> {profile[1]}\n"
                    f"<b>Статус:</b> {profile[4]}\n"
                    f"<b>Дата входа:</b> {dt.fromtimestamp(profile[7])}\n\n"
                    f"<blockquote>💵</blockquote>\n"
                    f"<b>Баланс:</b> {profile[6]}₽\n\n"
                    f"<blockquote>💰</blockquote>\n"
                    f"<b>Продаж:</b> {profile[8]}\n"
                    f"<b>Покупок:</b> {profile[9]}\n"
                    f"<b>Сумма покупок:</b> {profile[11]}₽\n"
                    f"<b>Сумма продаж:</b> {profile[10]}₽\n"
                    f"<b>Кол-во Отзывов:</b>\n    👍 - {positive}\n    👎 - {negative}\n"
                    f"<b>Споров:</b> {len(disputes)}\n"
                    f"<b>Выиграно:</b> {len(disputes_win)}", reply_markup=keyboard, parse_mode="HTML")

#Возврат в профиль
@dp.callback_query_handler(text_startswith="back_to_profile:", state="*")
async def mydeals(call: types.CallbackQuery, state: FSMContext):
    userid = int(call.data.split(":")[1])
    profile = await db.profile(userid)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"🤝 Мои сделки", callback_data=f"mydeals:{userid}"))
    keyboard.add(InlineKeyboardButton(f"🎁 Донаты", callback_data=f"donate:{userid}"), InlineKeyboardButton(f"🗣 Споры", callback_data=f"my_disputes:{userid}"))
    keyboard.add(InlineKeyboardButton(f"⬇️ Пополнить", callback_data=f"pays:{userid}"), InlineKeyboardButton(f"⬆️ Вывести", callback_data=f"my_payouts:{userid}"))
    feedbacks = await db.feedbacks(userid)
    positive = 0
    negative = 0
    disputes = await db.disputes_count(userid)
    disputes_win = await db.disputes_win(userid)
    if (len(feedbacks) != 0):
        for i in range(len(feedbacks)):
            if (feedbacks[i][3] == "👍"):
                positive += 1
            elif (feedbacks[i][3] == "👎"):
                negative += 1
    await call.message.edit_text("<blockquote>👤</blockquote>\n"
                    f"<b>Пользователь:</b> @{profile[3]}\n"
                    f"<b>ID:</b> {profile[1]}\n"
                    f"<b>Статус:</b> {profile[4]}\n"
                    f"<b>Дата входа:</b> {dt.fromtimestamp(profile[7])}\n\n"
                    f"<blockquote>💵</blockquote>\n"
                    f"<b>Баланс:</b> {profile[6]}₽\n\n"
                    f"<blockquote>💰</blockquote>\n"
                    f"<b>Продаж:</b> {profile[8]}\n"
                    f"<b>Покупок:</b> {profile[9]}\n"
                    f"<b>Сумма покупок:</b> {profile[11]}₽\n"
                    f"<b>Сумма продаж:</b> {profile[10]}₽\n"
                    f"<b>Кол-во Отзывов:</b>\n    👍 - {positive}\n    👎 - {negative}\n"
                    f"<b>Споров:</b> {len(disputes)}\n"
                    f"<b>Выиграно:</b> {len(disputes_win)}", reply_markup=keyboard, parse_mode="HTML")

@dp.message_handler(text=['🔍 Найти user'])
async def find_user(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"По userid", callback_data=f"find_user:userid"))
    keyboard.add(InlineKeyboardButton(f"По @username", callback_data=f"find_user:username"))
    await message.answer(f"Выберите направление поиска:", reply_markup=keyboard)

@dp.message_handler(text=['💬 Помощь'])
async def find_user(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Есть вопрос?", url=f"https://google.com"), InlineKeyboardButton(f"Предложить идею", url=f"https://google.com"))
    keyboard.add(InlineKeyboardButton(f"Как пользоваться автогарантом?", url=f"https://google.com"))
    await message.answer("Помощь:", reply_markup=keyboard)
#------------------------------------КНОПКИ

#------------------------------------ПОПОЛНЕНИЕ БАЛАНСА
#Пополнение баланса
@dp.callback_query_handler(text_startswith="pays:", state="*")
async def pay(call: types.CallbackQuery, state: FSMContext):
    userid = int(call.data.split(":")[1])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Назад", callback_data=f"back_to_profile:{userid}"))
    await call.message.edit_text(f"Введите сумму, на которую хотите пополнить баланс!", reply_markup=keyboard)
    await PAY.sum.set()

#Сумма пополнения баланса
@dp.message_handler(state=PAY.sum)
async def pay(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Назад", callback_data=f"back_to_profile:{message.from_user.id}"))
    try:
        int(message.text)
        check = await db.profile(message.from_user.id)
        if(int(message.text) < 100):
            await message.answer(f"Ошибка! Сумма меньше 100₽!", reply_markup=keyboard)
            await PAY.sum.set()
        else:
            PRICE = types.LabeledPrice(label=f"Пополнение баланса на {message.text}₽", amount=int(message.text)*100)  # в копейках (руб)
            await bot.send_invoice(message.chat.id,
                           title="Пополнение баланса",
                           description=f"Пополнение баланса на {message.text}₽",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="update-balance",
                           payload="test-invoice-payload")
            await state.finish()
    except ValueError:
        await message.answer("Введите число!", reply_markup=keyboard)
        await PAY.sum.set()

#Пречекаут
@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

#Успешное пополнение
@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await bot.send_message(message.chat.id, f"Ваш баланс пополнен на сумму {message.successful_payment.total_amount // 100}₽")
    check = await db.profile(message.from_user.id)
    await db.upd_user("balance", check[6]+int(message.successful_payment.total_amount // 100), message.from_user.id)
#------------------------------------ПОПОЛНЕНИЕ БАЛАНСА

#------------------------------------ДОНАТЫ
#Донаты
@dp.callback_query_handler(text_startswith="donate:", state="*")
async def donate(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    userid = int(call.data.split(":")[1])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"💰Пожертвовать", callback_data=f"donates:pay:{userid}"))
    keyboard.add(InlineKeyboardButton(f"🥇Топ донатов", callback_data=f"donates:top:{userid}"))
    keyboard.add(InlineKeyboardButton(f"Назад", callback_data=f"back_to_profile:{userid}"))
    await call.message.edit_text(f"🔅Все пожертвования пойдут на Развитие Проекта, закуп рекламы и т.п.\n\n🔅Благодарим за любую помощь проекту. Спасибо, что вы с нами!", reply_markup=keyboard)

#Задонатить/Вывод топа донатеров
@dp.callback_query_handler(text_startswith="donates:", state="*")
async def donate(call: types.CallbackQuery, state: FSMContext):
    type = call.data.split(":")[1]
    userid = int(call.data.split(":")[2])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Назад", callback_data=f"donate:{userid}"))
    if (type == "pay"):
        await call.message.edit_text("Введите сумму доната числом (от 10₽)", reply_markup=keyboard, parse_mode="Markdown")
        await Donate_create.sum.set()
    elif (type == "top"):
        check = await db.top_donate()
        text = "🏆<b>Топ донатеров:</b>\n\n"
        if (len(check) != 0):
            for i in range(len(check)):
                text += f"<b>🔥 {i+1}) <a href='tg://user?id={check[i][1]}'>{check[i][2]}</a> {check[i][3]}₽</b>\n"
        else:
            text += "Донатеров пока что нет 😢"
        await call.message.edit_text(f"{text}", reply_markup=keyboard, parse_mode="HTML")

#Сумма доната
@dp.message_handler(state=Donate_create.sum)
async def my_payout(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Вернуться", callback_data=f"donate:{message.from_user.id}"))
    try:
        int(message.text)
        check = await db.profile(message.from_user.id)
        if (check[6] < int(message.text)):
            await message.answer(f"Ошибка! Сумма превышает ваш баланс!\nДоступная сумма к донату: {check[6]}", reply_markup=keyboard)
            await Donate_create.sum.set()
        elif(int(message.text) < 10):
            await message.answer(f"Ошибка! Сумма меньше 10₽!", reply_markup=keyboard)
            await Donate_create.sum.set()
        else:
            check_don = await db.check_donate(message.from_user.id)
            if (len(check_don) == 0):
                await db.create_donate(message.from_user.id, message.from_user.full_name, int(message.text))
                await message.answer(f"Донат успешно отправлен! Ты сделал наш проект чуточку лучше!", reply_markup=keyboard)
                await db.upd_user("balance", check[6]-int(message.text), message.from_user.id)
            else:
                await db.upd_donate(message.from_user.id, int(check_don[3])+int(message.text))
                await message.answer(f"Донат успешно отправлен! Ты сделал наш проект чуточку лучше!", reply_markup=keyboard)
                await db.upd_user("balance", check[6]-int(message.text), message.from_user.id)
            await state.finish()
    except ValueError:
        await message.answer("Введите число!", reply_markup=keyboard)
        await Donate_create.sum.set()
#------------------------------------ДОНАТЫ

#------------------------------------ПОЛЬЗОВАТЕЛЬ
#Выбор поиска пользователя
@dp.callback_query_handler(text_startswith="find_user:", state="*")
async def mydeals(call: types.CallbackQuery, state: FSMContext):
    type = call.data.split(":")[1]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Отмена", callback_data=f"cancel"))
    if (type == "userid"):
        await call.message.edit_text("Укажите userid. Вы можете попросить пользователя посмотреть его в профиле бота.", reply_markup=keyboard)
    elif (type == "username"):
        await call.message.edit_text("Укажите username *(без @)*. Вы можете попросить пользователя посмотреть его в профиле бота.", reply_markup=keyboard, parse_mode="Markdown")
    await FindUser.type.set()
    await state.update_data(type=type)

#Найденный пользователь. Инфо о нём
@dp.message_handler(state=FindUser.type)
async def user(message: types.Message, state: FSMContext):
    await state.update_data(find=message.text)
    data = await state.get_data()
    find_user = await db.find_user(data['type'], data['find'])
    keyboard = InlineKeyboardMarkup()
    check_admin = await db.check_admin(message.from_user.id)
    feedbacks = await db.feedbacks(find_user[1])
    positive = 0
    negative = 0
    rating = 0
    disputes = await db.disputes_count(find_user[1])
    disputes_win = await db.disputes_win(find_user[1])
    if (len(feedbacks) != 0):
        for i in range(len(feedbacks)):
            if (feedbacks[i][3] == "👍"):
                positive += 1
            elif (feedbacks[i][3] == "👎"):
                negative += 1
        rating = int((positive/len(feedbacks)*100))
    if (check_admin == 1):
        if (find_user[5] == 0):
            keyboard.add(InlineKeyboardButton(f"Назначить администратором", callback_data=f"admin:add:{find_user[1]}:{message.from_user.id}"))
        if (find_user[5] == 1):
            keyboard.add(InlineKeyboardButton(f"Снять администратора", callback_data=f"admin:del:{find_user[1]}:{message.from_user.id}"))
    keyboard.add(InlineKeyboardButton(f"Оформить сделку", callback_data=f"deal_create:{find_user[1]}:{message.from_user.id}"))
    keyboard.add(InlineKeyboardButton(f"Отзывы", callback_data=f"feedback:{find_user[1]}:{message.from_user.id}"))
    if (find_user == "Произошла ошибка! Перепроверьте данные и попробуйте снова!"):
        await message.answer("Произошла ошибка! Перепроверьте данные и попробуйте снова!")
    elif (find_user):
        text =  f"<blockquote>👤</blockquote>\n"
        text +=  f"<b>Статус:</b> {find_user[4]}\n"
        text +=  f"<b>Юзер </b><a href='tg://user?id={find_user[1]}'>{find_user[2]}</a>\n"
        text +=  f"<b>Дата входа:</b> {dt.fromtimestamp(find_user[7])}\n\n"
        text +=  f"<blockquote>💰</blockquote>\n" 
        text +=  f"<b>Кол-во Отзывов:</b>\n    👍 - {positive}\n    👎 - {negative}\n"
        text +=  f"<b>Рейтинг:</b> {rating}%\n\n"
        text +=  f"<b>Продаж:</b> {find_user[8]} шт.\n"
        text +=  f"<b>Покупок:</b> {find_user[9]} шт.\n"
        text +=  f"<b>Сумма покупок:</b> {find_user[11]} руб.\n"
        text +=  f"<b>Сумма продаж:</b> {find_user[10]} руб.\n\n"
        text +=  f"<blockquote>📂</blockquote>\n"
        text +=  f"<b>Споров: {len(disputes)}</b>\n"
        text +=  f"<b>Выиграно: {len(disputes_win)}</b>"
        if (find_user[1] == message.from_user.id):
            await message.answer(text, parse_mode="HTML")
        else:
            await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await message.answer("Данный пользователь не найден!")
    await state.finish()

#Возврат к найденному пользователю. Инфо о нём
@dp.callback_query_handler(text_startswith="back_to_user:", state="*")
async def back_to_user(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    userid = int(call.data.split(":")[1])
    my_userid = int(call.data.split(":")[2])
    find_user = await db.find_user('userid', userid)
    keyboard = InlineKeyboardMarkup()
    feedbacks = await db.feedbacks(userid)
    check_admin = await db.check_admin(my_userid)
    positive = 0
    negative = 0
    rating = 0
    disputes = await db.disputes_count(userid)
    disputes_win = await db.disputes_win(userid)
    if (len(feedbacks) != 0):
        for i in range(len(feedbacks)):
            if (feedbacks[i][3] == "👍"):
                positive += 1
            elif (feedbacks[i][3] == "👎"):
                negative += 1
        rating = int((positive/len(feedbacks)*100))
    if (check_admin == 1):
        if (find_user[5] == 0):
            keyboard.add(InlineKeyboardButton(f"Назначить администратором", callback_data=f"admin:add:{find_user[1]}:{my_userid}"))
        if (find_user[5] == 1):
            keyboard.add(InlineKeyboardButton(f"Снять администратора", callback_data=f"admin:del:{find_user[1]}:{my_userid}"))
    keyboard.add(InlineKeyboardButton(f"Оформить сделку", callback_data=f"deal_create:{find_user[1]}:{my_userid}"))
    keyboard.add(InlineKeyboardButton(f"Отзывы", callback_data=f"feedback:{find_user[1]}:{my_userid}"))
    text =  f"<blockquote>👤</blockquote>\n"
    text +=  f"<b>Статус:</b> {find_user[4]}\n"
    text +=  f"<b>Юзер </b><a href='tg://user?id={find_user[1]}'>{find_user[2]}</a>\n"
    text +=  f"<b>Дата входа:</b> {dt.fromtimestamp(find_user[7])}\n\n"
    text +=  f"<blockquote>💰</blockquote>\n" 
    text +=  f"<b>Кол-во Отзывов:</b>\n    👍 - {positive}\n    👎 - {negative}\n"
    text +=  f"<b>Рейтинг:</b> {rating}%\n\n"
    text +=  f"<b>Продаж:</b> {find_user[8]} шт.\n"
    text +=  f"<b>Покупок:</b> {find_user[9]} шт.\n"
    text +=  f"<b>Сумма покупок:</b> {find_user[11]} руб.\n"
    text +=  f"<b>Сумма продаж:</b> {find_user[10]} руб.\n\n"
    text +=  f"<blockquote>📂</blockquote>\n"
    text +=  f"<b>Споров: {len(disputes)}</b>\n"
    text +=  f"<b>Выиграно: {len(disputes_win)}</b>"
    if (find_user[1] == my_userid):
        await call.message.edit_text(text, parse_mode="HTML")
    else:
        await call.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")

#Вывод отзывов
@dp.callback_query_handler(text_startswith="feedback:", state="*")
async def feed(call: types.CallbackQuery, state: FSMContext):
    userid = int(call.data.split(":")[1])
    my_userid = int(call.data.split(":")[2])
    list = await func.feedback(userid, 0, my_userid)
    await call.message.edit_text(list[0], reply_markup=list[1], parse_mode="Markdown")

#Нзначить/снять админа
@dp.callback_query_handler(text_startswith="admin:", state="*")
async def admin(call: types.CallbackQuery, state: FSMContext):
    type = call.data.split(":")[1]
    userid = int(call.data.split(":")[2])
    my_userid = int(call.data.split(":")[3])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Вернуться к пользователю", callback_data=f"back_to_user:{userid}:{my_userid}"))
    if (type == "add"):
        await db.upd_user("is_admin", 1, userid)
        await db.upd_user_adm("status", "Admin", userid)
        await call.message.edit_text("Пользователь назначен администратором!", reply_markup=keyboard)
        await bot.send_message(userid, "Вас назначили на должность администратора!", reply_markup=AmainMenu)
    elif (type == "del"):
        await db.upd_user("is_admin", 0, userid)
        await db.upd_user_adm("status", "User", userid)
        await call.message.edit_text("Пользователь снят с должности администратора!", reply_markup=keyboard)
        await bot.send_message(userid, "Вас сняли с должности администратора!", reply_markup=mainMenu)


#Создание сделки. Выбор типа
@dp.callback_query_handler(text_startswith="deal_create:", state="*")
async def feed(call: types.CallbackQuery, state: FSMContext):
    userid = int(call.data.split(":")[1])
    my_userid = int(call.data.split(":")[2])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Я покупатель", callback_data=f"deal:buyer:{userid}:{my_userid}"))
    keyboard.add(InlineKeyboardButton(f"Я продавец", callback_data=f"deal:seller:{userid}:{my_userid}"))
    keyboard.add(InlineKeyboardButton(f"Вернуться к пользователю", callback_data=f"back_to_user:{userid}:{my_userid}"))
    await call.message.edit_text("*❔Выберите кем вы будете выступать в сделке.*", reply_markup=keyboard, parse_mode="Markdown")
#------------------------------------ПОЛЬЗОВАТЕЛЬ

#------------------------------------СДЕЛКИ
#Создание сделки. Указание суммы
@dp.callback_query_handler(text_startswith="deal:", state="*")
async def feed(call: types.CallbackQuery, state: FSMContext):
    type = call.data.split(":")[1]
    userid = int(call.data.split(":")[2])
    my_userid = int(call.data.split(":")[3])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Вернуться к пользователю", callback_data=f"back_to_user:{userid}:{my_userid}"))
    name = await db.profile(userid)
    my_name = await db.profile(my_userid)
    if (type == "buyer"):
        await call.message.edit_text("*Укажите сумму сделки (Минимальная сумма - 100 руб)*", reply_markup=keyboard, parse_mode="Markdown")
        await DealCreate.sum.set()
        await state.update_data(buyer_userid=my_userid)
        await state.update_data(seller_userid=userid)
        await state.update_data(buyer_name=my_name[2])
        await state.update_data(seller_name=name[2])
        await state.update_data(i_am=type)
    elif (type == "seller"):
        await call.message.edit_text("*Укажите сумму сделки (Минимальная сумма - 100 руб)*", reply_markup=keyboard, parse_mode="Markdown")
        await DealCreate.sum.set()
        await state.update_data(buyer_userid=userid)
        await state.update_data(seller_userid=my_userid)
        await state.update_data(buyer_name=name[2])
        await state.update_data(seller_name=my_name[2])
        await state.update_data(i_am=type)

#Создание сделки. Указание условий
@dp.message_handler(state=DealCreate.sum)
async def user(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = InlineKeyboardMarkup()
    if (data['i_am'] == "seller"):
        my_userid = int(data['seller_userid'])
        userid = int(data['buyer_userid'])
    elif(data['i_am'] == "buyer"):
        my_userid = int(data['buyer_userid'])
        userid = int(data['seller_userid'])
    keyboard.add(InlineKeyboardButton(f"Вернуться к пользователю", callback_data=f"back_to_user:{userid}:{my_userid}"))
    if (int(message.text) < 100):
        await message.answer("*Указанная сумма меньше 100 руб.\nУкажите сумму меньше либо равную 100 руб*", reply_markup=keyboard, parse_mode="Markdown")
        await DealCreate.sum.set()
    else:
        await state.update_data(sum=message.text)
        await message.answer("*Введите условия сделки (Продажа аккаунта VK, Покупка схемы заработка и т.д)*", reply_markup=keyboard, parse_mode="Markdown")
        await DealCreate.desc.set()

#Создание сделки. Отправка подтверждения
@dp.message_handler(state=DealCreate.desc)
async def user(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)
    data = await state.get_data()
    id = await db.add_deal(int(data['seller_userid']), int(data['buyer_userid']), data['seller_name'], data['buyer_name'], data['desc'], int(data['sum']))
    await message.answer(f"Запрос на сделку №{id}\n"
                    f"Продавец: <a href='tg://user?id={int(data['seller_userid'])}'>{data['seller_name']}</a>\n"
                    f"Покупатель: <a href='tg://user?id={int(data['buyer_userid'])}'>{data['buyer_name']}</a>\n"
                    f"Сумма: {int(data['sum'])}₽\n"
                    f"Условия: {data['desc']}"
                    "<blockquote>➖➖➖➖➖➖➖\n"
                    "❗️Это запрос на сделку, его нужно оплатить, чтобы сделка началась.\n\n"
                    "❓Не используйте платёжные реквизиты или контактную информацию из этого сообщения.\n\n"
                    "Внимание:\n"
                    "Это всего лишь неоплаченный запрос на сделку!\n"
                    "➖➖➖➖➖➖➖</blockquote>", parse_mode="HTML")
    if (data['i_am'] == "seller"):
        userid = int(data['buyer_userid'])
        sec_userid = int(data['seller_userid'])
    elif (data['i_am'] == "buyer"):
        userid = int(data['seller_userid'])
        sec_userid = int(data['buyer_userid'])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"✅ Принять", callback_data=f"deal_msg:accept:{id}:{userid}:{sec_userid}"), InlineKeyboardButton(f"❌ Отклонить", callback_data=f"deal_msg:decline:{id}:{userid}:{sec_userid}"))
    await bot.send_message(userid, f"Запрос на сделку №{id}\n"
                    f"Продавец: <a href='tg://user?id={int(data['seller_userid'])}'>{data['seller_name']}</a>\n"
                    f"Покупатель: <a href='tg://user?id={int(data['buyer_userid'])}'>{data['buyer_name']}</a>\n"
                    f"Сумма: {int(data['sum'])}₽\n"
                    f"Условия: {data['desc']}"
                    "<blockquote>➖➖➖➖➖➖➖\n"
                    "❗️Это запрос на сделку, его нужно оплатить, чтобы сделка началась.\n\n"
                    "❓Не используйте платёжные реквизиты или контактную информацию из этого сообщения.\n\n"
                    "Внимание:\n"
                    "Это всего лишь неоплаченный запрос на сделку!\n"
                    "➖➖➖➖➖➖➖</blockquote>", reply_markup=keyboard, parse_mode="HTML")
    await state.finish()

#Создание сделки. Отправка оплаты
@dp.callback_query_handler(text_startswith="deal_msg:", state="*")
async def deal_msg(call: types.CallbackQuery, state: FSMContext):
    type = call.data.split(":")[1]
    deal_id = int(call.data.split(":")[2])
    my_userid = int(call.data.split(":")[3])
    userid = int(call.data.split(":")[4])
    deal = await db.deal(deal_id)
    if (type == "accept"):
        await db.upd_deal(deal_id, 1)
        keyboard = InlineKeyboardMarkup()
        if(deal[2] == my_userid):
            keyboard.add(InlineKeyboardButton(f"Оплатить", callback_data=f"deal_pay:{deal_id}:{my_userid}:{userid}"))
            await call.message.edit_text(f"Оплата сделки №{deal_id}\n"
                    f"Продавец: <a href='tg://user?id={deal[1]}'>{deal[3]}</a>\n"
                    f"Покупатель: <a href='tg://user?id={deal[2]}'>{deal[4]}</a>\n"
                    f"Сумма: {deal[6]*1.05}₽\n"
                    f"Условия: {deal[5]}"
                    "<blockquote>➖➖➖➖➖➖➖\n"
                    "❗️Это запрос на сделку, его нужно оплатить, чтобы сделка началась.\n\n"
                    "❓Не используйте платёжные реквизиты или контактную информацию из этого сообщения.\n\n"
                    "Внимание:\n"
                    "Это всего лишь неоплаченный запрос на сделку!\n"
                    "➖➖➖➖➖➖➖</blockquote>", reply_markup=keyboard, parse_mode="HTML")
        elif(deal[2] == userid):
            keyboard.add(InlineKeyboardButton(f"Оплатить", callback_data=f"deal_pay:{deal_id}:{userid}:{my_userid}"))
            await call.message.edit_text("Ожидаем оплаты покупателя")
            await bot.send_message(userid, f"Оплата сделки №{deal_id}\n"
                    f"Продавец: <a href='tg://user?id={deal[1]}'>{deal[3]}</a>\n"
                    f"Покупатель: <a href='tg://user?id={deal[2]}'>{deal[4]}</a>\n"
                    f"Сумма: {deal[6]*1.05}₽\n"
                    f"Условия: {deal[5]}"
                    "<blockquote>➖➖➖➖➖➖➖\n"
                    "❗️Это запрос на сделку, его нужно оплатить, чтобы сделка началась.\n\n"
                    "❓Не используйте платёжные реквизиты или контактную информацию из этого сообщения.\n\n"
                    "Внимание:\n"
                    "Это всего лишь неоплаченный запрос на сделку!\n"
                    "➖➖➖➖➖➖➖</blockquote>", reply_markup=keyboard, parse_mode="HTML")
    elif(type == "decline"):
        await bot.send_message(userid, f"Сделка №{deal_id} была отменена")
        await call.message.edit_text(f"Запрос на сделку №{deal_id} был отменён!")
        await db.del_deal(deal_id)

#Создание сделки. Оплата сделки
@dp.callback_query_handler(text_startswith="deal_pay:", state="*")
async def deal_pay(call: types.CallbackQuery, state: FSMContext):
    deal_id = int(call.data.split(":")[1])
    my_userid = int(call.data.split(":")[2])
    userid = int(call.data.split(":")[3])
    cur_balance = await db.profile(my_userid)
    deal = await db.deal(deal_id)
    keyboard = InlineKeyboardMarkup()
    kb = InlineKeyboardMarkup()
    if (cur_balance[6] < deal[6]*1.05):
        await call.message.answer("*Ваш баланс меньше суммы сделки!\n Для продолжения пополните баланс!*", parse_mode="Markdown")
    else:
        keyboard.add(InlineKeyboardButton(f"Отправить товар покупателю", callback_data=f"deal_send:{deal_id}:{my_userid}:{userid}"))
        await db.upd_user("balance", cur_balance[6] - deal[6]*1.05, my_userid)
        kb.add(InlineKeyboardButton(f"Открыть спор", callback_data=f"dispute:{deal_id}:{my_userid}:{userid}:buyer"))
        await call.message.edit_text(f"Сделка №{deal_id} успешно оплачена! \nОжидайте передачи данных от продавца!", reply_markup=kb)
        await bot.send_message(userid, f"Сделка №{deal_id} успешно оплачена!", reply_markup=keyboard)
        await db.upd_deal(deal_id, 2)

#Создание сделки. Отправить товар покупателю
@dp.callback_query_handler(text_startswith="deal_send:", state="*")
async def deal_send(call: types.CallbackQuery, state: FSMContext):
    deal_id = int(call.data.split(":")[1])
    userid = int(call.data.split(":")[2])
    my_userid = int(call.data.split(":")[3])
    await call.message.edit_text("Отправьте покупку файлом/текстом/картинкой покупателю")
    await DealSend.send.set()
    await state.update_data(seller_userid=my_userid)
    await state.update_data(buyer_userid=userid)
    await state.update_data(deal_id=deal_id)

#Создание сделки. Отправка товара
@dp.message_handler(state=DealSend.send)
async def deal_send(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.copy_message(chat_id=int(data['buyer_userid']), from_chat_id=message.chat.id, message_id=message.message_id)
    await db.upd_deal(int(data['deal_id']), 3)
    keyboard = InlineKeyboardMarkup()
    keyboard2 = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"✅Подтвердить сделку", callback_data=f"deal_finish:accept:{int(data['deal_id'])}:{int(data['seller_userid'])}:{int(data['buyer_userid'])}"))
    keyboard.add(InlineKeyboardButton(f"Открыть спор", callback_data=f"dispute:{int(data['deal_id'])}:{int(data['seller_userid'])}:{int(data['buyer_userid'])}:buyer"))
    keyboard2.add(InlineKeyboardButton(f"Открыть спор", callback_data=f"dispute:{int(data['deal_id'])}:{int(data['seller_userid'])}:{int(data['buyer_userid'])}:seller"))
    await bot.send_message(int(data['buyer_userid']), f"Продавец отправил вам покупку! Внимательно проверьте её перед подтверждением!", reply_markup=keyboard)
    await message.answer("Ожидайте подтверждения сделки от покупателя.", reply_markup=keyboard2)
    await state.finish()

#Завершение сделки/Открытие спора
@dp.callback_query_handler(text_startswith="deal_finish:", state="*")
async def deal_finish(call: types.CallbackQuery, state: FSMContext):
    type = call.data.split(":")[1]
    deal_id = int(call.data.split(":")[2])
    seller = int(call.data.split(":")[3])
    buyer = int(call.data.split(":")[4])
    from_type = call.data.split(":")[5]
    seller_profile = await db.profile(seller)
    buyer_profile = await db.profile(buyer)
    deal = await db.deal(deal_id)
    keyboard = InlineKeyboardMarkup()
    if (type == "accept"):
        keyboard.add(InlineKeyboardButton(f"Оставить отзыв", callback_data=f"deal_feedback:{seller}:{buyer}"))
        await db.upd_user("balance", seller_profile[6]+(deal[6]), seller)
        await db.upd_user("sell", seller_profile[8]+1, seller)
        await db.upd_user("sum_sell", seller_profile[10]+deal[6], seller)
        await db.upd_user("buy", buyer_profile[9]+1, buyer)
        await db.upd_user("sum_buy", buyer_profile[10]+deal[6], buyer)
        await db.upd_deal(deal_id, 5)
        await call.message.edit_text("Сделка успешно завершена!\nВы также можете оставить отзыв о продавце!", reply_markup=keyboard)
        await bot.send_message(seller, f"Сделка успешно завершена!\nВаш баланс пополнен на {deal[6]}₽")
    elif (type == "dispute"):
        check = await db.check_disp(deal_id)
        if (from_type == "seller"):
            if (len(check) == 0):
                await call.message.edit_text("Укажите причину спора:")
                await Dispute_Add.desc.set()
                await state.update_data(from_user="seller")
                await state.update_data(seller_userid=seller_profile[1])
                await state.update_data(buyer_userid=buyer_profile[1])
                await state.update_data(seller_name=seller_profile[2])
                await state.update_data(buyer_name=buyer_profile[2])
                await state.update_data(deal_id=deal_id)
            else:
                keyboard.add(InlineKeyboardButton(f"К спорам", callback_data=f"my_disputes:{seller_profile[1]}"))
                await call.message.edit_text("Уже есть открытый спор по поводу данной сделки!", reply_markup=keyboard)
        elif (from_type == "buyer"):
            if (len(check) == 0):
                await call.message.edit_text("Укажите причину спора:")
                await Dispute_Add.desc.set()
                await state.update_data(from_user="buyer")
                await state.update_data(seller_userid=seller_profile[1])
                await state.update_data(buyer_userid=buyer_profile[1])
                await state.update_data(seller_name=seller_profile[2])
                await state.update_data(buyer_name=buyer_profile[2])
                await state.update_data(deal_id=deal_id)
            else:
                keyboard.add(InlineKeyboardButton(f"К спорам", callback_data=f"my_disputes:{buyer_profile[1]}"))
                await call.message.edit_text("Уже есть открытый спор по поводу данной сделки!", reply_markup=keyboard)
#------------------------------------СДЕЛКИ

#------------------------------------СПОРЫ
#Спор. Подтверждение
@dp.callback_query_handler(text_startswith="dispute:", state="*")
async def dispute(call: types.CallbackQuery, state: FSMContext):
    deal_id = int(call.data.split(":")[1])
    seller = int(call.data.split(":")[2])
    buyer = int(call.data.split(":")[3])
    from_type = call.data.split(":")[4]
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(f"Да", callback_data=f"deal_finish:dispute:{deal_id}:{seller}:{buyer}:{from_type}"))
    kb.add(InlineKeyboardButton(f"Нет", callback_data=f"back_to_finish:{deal_id}:{seller}:{buyer}:{from_type}"))
    await call.message.edit_text("Вы уверены?", reply_markup=kb)

#Спор. Нет
@dp.callback_query_handler(text_startswith="back_to_finish:", state="*")
async def dispute_no(call: types.CallbackQuery, state: FSMContext):
    deal_id = int(call.data.split(":")[1])
    seller = int(call.data.split(":")[2])
    buyer = int(call.data.split(":")[3])
    from_type = call.data.split(":")[4]
    keyboard = InlineKeyboardMarkup()
    keyboard2 = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"✅Подтвердить сделку", callback_data=f"deal_finish:accept:{deal_id}:{seller}:{buyer}"))
    keyboard.add(InlineKeyboardButton(f"Открыть спор", callback_data=f"dispute:{deal_id}:{seller}:{buyer}:buyer"))
    keyboard2.add(InlineKeyboardButton(f"Открыть спор", callback_data=f"dispute:{deal_id}:{seller}:{buyer}:seller"))
    if (from_type == "seller"):
        await call.message.edit_text("Ожидайте подтверждения сделки от покупателя.", reply_markup=keyboard2)
    elif (from_type == "buyer"):
        await call.message.edit_text(f"Продавец отправил вам покупку! Внимательно проверьте её перед подтверждением!", reply_markup=keyboard)

#Спор. Причина
@dp.message_handler(state=Dispute_Add.desc)
async def dispute_create(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)
    data = await state.get_data()
    await db.dispute_add(data['from_user'], int(data['seller_userid']), int(data['buyer_userid']), data['seller_name'], data['buyer_name'], int(data['deal_id']), data['desc'])
    keyboard = InlineKeyboardMarkup()
    if (data['from_user'] == "seller"):
        keyboard.add(InlineKeyboardButton(f"Перейти к спорам", callback_data=f"my_disputes:{int(data['buyer_userid'])}"))
        await bot.send_message(int(data['buyer_userid']), f"На вас открыт спор по поводу сделки №{int(data['deal_id'])}", reply_markup=keyboard)
    elif (data['from_user'] == "buyer"):
        keyboard.add(InlineKeyboardButton(f"Перейти к спорам", callback_data=f"my_disputes:{int(data['seller_userid'])}"))
        await bot.send_message(int(data['seller_userid']), f"На вас открыт спор по поводу сделки №{int(data['deal_id'])}", reply_markup=keyboard)
    keyboard.add(InlineKeyboardButton(f"Перейти к спорам", callback_data=f"my_disputes:{message.from_user.id}"))
    await message.answer(f"Вы открыли спор по поводу сделки №{int(data['deal_id'])}", reply_markup=keyboard)
    await state.finish()

#Спор. Мои споры
@dp.callback_query_handler(text_startswith="my_disputes:", state="*")
async def my_disputes(call: types.CallbackQuery, state: FSMContext):
    userid = int(call.data.split(":")[1])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Активные споры", callback_data=f"disputes_type:active:{userid}"), InlineKeyboardButton(f"Завершённые споры", callback_data=f"disputes_type:closed:{userid}"))
    keyboard.add(InlineKeyboardButton(f"Вернуться в профиль", callback_data=f"back_to_profile:{userid}"))
    await call.message.edit_text("Выберите какие споры хотите посмотреть", reply_markup=keyboard)

#Спор. Выбор типа спора
@dp.callback_query_handler(text_startswith="disputes_type:", state="*")
async def my_disputes(call: types.CallbackQuery, state: FSMContext):
    type = call.data.split(":")[1]
    userid = int(call.data.split(":")[2])
    if (type == "active"):
        await call.message.edit_text("Выберите нужный спор", reply_markup=await func.my_disputes(userid, 0, 0))
    elif (type == "closed"):
        await call.message.edit_text("Выберите нужный спор", reply_markup=await func.my_disputes(userid, 0, 1))

#Спор. Добавление сообщений
@dp.callback_query_handler(text_startswith="disp_add_msg:", state="*")
async def disp_add_msg(call: types.CallbackQuery, state: FSMContext):
    deal_id = int(call.data.split(":")[1])
    userid = int(call.data.split(":")[2])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Отмена", callback_data=f"my_disp_open:{userid}:{deal_id}"))
    await call.message.edit_text("Введите ваше сообщение ниже:", reply_markup=keyboard)
    await Dispute_Msg.text.set()
    await state.update_data(deal_id=deal_id)

#Спор. Сообщение
@dp.message_handler(state=Dispute_Msg.text)
async def disp_add_msg(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Вернуться к спору", callback_data=f"my_disp_open:{message.from_user.id}:{int(data['deal_id'])}"))
    check = await db.dispute_from(int(data['deal_id']))
    if (check[2] == message.from_user.id):
        await db.dispute_add_msg("seller", data['text'], int(data['deal_id']))
        await bot.send_message(check[3], f"Продавец оставил сообщение в споре о сделке №{int(data['deal_id'])}")
    if (check[3] == message.from_user.id):
        await db.dispute_add_msg("buyer", data['text'], int(data['deal_id']))
        await bot.send_message(check[2], f"Покупатель оставил сообщение в споре о сделке №{int(data['deal_id'])}")
    await message.answer("Сообщение добавлено!", reply_markup=keyboard)

#Спор. Открытие моих споров
@dp.callback_query_handler(text_startswith="my_disp_open:", state="*")
async def my_disputes(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    userid = int(call.data.split(":")[1])
    deal_id = int(call.data.split(":")[2])
    disp = await func.my_disp_open(deal_id, 0, userid)
    await call.message.edit_text(disp[0], reply_markup=disp[1], parse_mode="Markdown")
#------------------------------------СПОРЫ

#------------------------------------ОТЗЫВЫ
#Отзывы. Выбор оценки
@dp.callback_query_handler(text_startswith="deal_feedback:", state="*")
async def deal_feedback(call: types.CallbackQuery, state: FSMContext):
    seller = int(call.data.split(":")[1])
    buyer = int(call.data.split(":")[2])
    btn1 = KeyboardButton('👍')
    btn2 = KeyboardButton('👎')
    type = ReplyKeyboardMarkup(resize_keyboard = True).add(btn1, btn2)
    await call.message.delete()
    await call.message.answer("*Выберите оценку*", reply_markup=type, parse_mode="Markdown")
    await FeedBack_add.type.set()
    await state.update_data(seller_userid = seller)
    await state.update_data(buyer_userid = buyer)

#Отзывы. Тип отзыва
@dp.message_handler(state=FeedBack_add.type)
async def deal_feedback(message: types.Message, state: FSMContext):
    if (message.text == '👍'):
        await state.update_data(type=message.text)
        await message.answer("Напишите ваш отзыв", reply_markup=ReplyKeyboardRemove(), parse_mode="markdown")
        await FeedBack_add.text.set()
    elif (message.text == '👎'):
        await state.update_data(type=message.text)
        await message.answer("Напишите ваш отзыв", reply_markup=ReplyKeyboardRemove(), parse_mode="markdown")
        await FeedBack_add.text.set()

#Отзывы. Добавление отзыва
@dp.message_handler(state=FeedBack_add.text)
async def deal_feedback(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    check = await db.check_admin(int(data['buyer_userid']))
    await db.add_feedback(int(data['seller_userid']), int(data['buyer_userid']), data['type'], data['text'])
    if (check == 1):
        await message.answer("Отзыв успешно отправлен!", reply_markup=AmainMenu)
        await bot.send_message(int(data['seller_userid']), "Покупатель оставил вам отзыв!")
    else:
        await message.answer("Отзыв успешно отправлен!", reply_markup=mainMenu)
        await bot.send_message(int(data['seller_userid']), "Покупатель оставил вам отзыв!")
    await state.finish()
#------------------------------------ОТЗЫВЫ

#------------------------------------ВЫВОД СРЕДСТВ
#Заявки на вывод средств просмотр/создать
@dp.callback_query_handler(text_startswith="my_payouts:", state="*")
async def my_payouts(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    userid = int(call.data.split(":")[1])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Активные", callback_data=f"my_payout:active:{userid}"), InlineKeyboardButton(f"Завершённые", callback_data=f"my_payout:finished:{userid}"))
    keyboard.add(InlineKeyboardButton(f"Создать заявку", callback_data=f"my_payout:create:{userid}"))
    keyboard.add(InlineKeyboardButton(f"👈Вернуться в профиль", callback_data=f"back_to_profile:{userid}"))
    await call.message.edit_text(f"Выберите тип для просмотра заявок или создайте новую", reply_markup=keyboard)

#Создание вывода, вывод заявок
@dp.callback_query_handler(text_startswith="my_payout:", state="*")
async def my_payout(call: types.CallbackQuery, state: FSMContext):
    type = call.data.split(":")[1]
    userid = int(call.data.split(":")[2])
    if (type == "active"):
        pays = await func.my_payouts(userid, 0, 0)
        await call.message.edit_text(pays[0], reply_markup=pays[1], parse_mode="Markdown")
    elif(type == "finished"):
        pays = await func.my_payouts(userid, 0, 1)
        await call.message.edit_text(pays[0], reply_markup=pays[1], parse_mode="Markdown")
    elif (type == "create"):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(f"Вернуться", callback_data=f"my_payouts:{userid}"))
        await call.message.edit_text("Введите номер карты/номер телефона и банк куда вывести в формате: *+79999999999 СберБанк*", reply_markup=keyboard, parse_mode="Markdown")
        await Payout_create.text.set()

#Сумма вывода
@dp.message_handler(state=Payout_create.text)
async def my_payout(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Вернуться", callback_data=f"my_payouts:{message.from_user.id}"))
    await message.answer("Введите сумму вывода числом", reply_markup=keyboard)
    await Payout_create.sum.set()

#Сумма вывода
@dp.message_handler(state=Payout_create.sum)
async def my_payout(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Вернуться", callback_data=f"my_payouts:{message.from_user.id}"))
    try:
        int(message.text)
        check = await db.profile(message.from_user.id)
        if (check[6] < int(message.text)):
            await message.answer(f"Ошибка! Сумма превышает ваш баланс!\nДоступная сумма к выводу: {check[6]}", reply_markup=keyboard)
            await Payout_create.sum.set()
        elif (int(message.text) <= 0):
            await message.answer(f"Ошибка! Сумма не может быть *меньше или равно нулю*!\n*Доступная сумма к выводу:* {check[6]}", reply_markup=keyboard, parse_mode="Markdown")
            await Payout_create.sum.set()
        else:
            data = await state.get_data()
            await db.create_payout(message.from_user.id, message.from_user.full_name, int(message.text), data['text'])
            await db.upd_user("balance", check[6]-int(message.text), message.from_user.id)
            await message.answer(f"Заявка на вывод успешно создана!", reply_markup=keyboard)
            await state.finish()
    except ValueError:
        await message.answer("Введите число!", reply_markup=keyboard)
        await Payout_create.sum.set()
#------------------------------------ВЫВОД СРЕДСТВ

#------------------------------------ОБРАБОТЧИКИ
#Отмена
@dp.callback_query_handler(text_startswith="cancel", state="*")
async def mydeals(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    await call.message.edit_text("Отменено!")

#Вывод сделок
@dp.callback_query_handler(text_startswith="mydeals:", state="*")
async def mydeals(call: types.CallbackQuery, state: FSMContext):
    userid = int(call.data.split(":")[1])
    deals = await func.my_deals(userid, 0)
    await call.message.edit_text(deals[0], reply_markup=deals[1], parse_mode="HTML")

#Далее/Назад сделки
@dp.callback_query_handler(text_startswith="deal_swipe:", state="*")
async def NextOrBack(call: types.CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    userid = int(call.data.split(":")[2])
    await call.message.edit_text("Ваши сделки:", reply_markup=await func.my_deals(userid, remover))

#Далее/Назад отзывы
@dp.callback_query_handler(text_startswith="feed_swipe:", state="*")
async def NextOrBack(call: types.CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    userid = int(call.data.split(":")[2])
    my_userid = int(call.data.split(":")[3])
    list = await func.feedback(userid, remover, my_userid)
    await call.message.edit_text(list[0], reply_markup=list[1], parse_mode="Markdown")

#Далее/Назад споры
@dp.callback_query_handler(text_startswith="disp_swipe:", state="*")
async def NextOrBack(call: types.CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    userid = int(call.data.split(":")[2])
    status = int(call.data.split(":")[3])
    list = await func.my_disputes(userid, remover, status)
    await call.message.edit_text(list[0], reply_markup=list[1], parse_mode="Markdown")

#Далее/Назад сообщения в спорах
@dp.callback_query_handler(text_startswith="dispute_swipe:", state="*")
async def NextOrBack(call: types.CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    deal_id = int(call.data.split(":")[2])
    userid = int(call.data.split(":")[3])
    list = await func.my_disp_open(deal_id, remover, userid)
    await call.message.edit_text(list[0], reply_markup=list[1], parse_mode="Markdown")

#Далее/Назад заявки на вывод
@dp.callback_query_handler(text_startswith="payouts_swipe:", state="*")
async def NextOrBack(call: types.CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    userid = int(call.data.split(":")[2])
    status = int(call.data.split(":")[3])
    list = await func.my_payouts(userid, remover, status)
    await call.message.edit_text(list[0], reply_markup=list[1], parse_mode="Markdown")
#------------------------------------ОБРАБОТЧИКИ