from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import db

#Вывод сделок юзера
async def my_deals(userid, remover):

    list_deals = await db.mydeals(userid)
    keyboard = InlineKeyboardMarkup()
    deals = "*Ваши сделки:*\n\n"
    if (len(list_deals) != 0):
        if remover >= len(list_deals): remover -= 7

        for count, a in enumerate(range(remover, len(list_deals))):
            status = ""
            if count < 7:
                deals += f"<b>Сделка №{list_deals[count][0]}</b>\n"
                deals += f"<b>Продавец:</b> <a href='tg://user?id={list_deals[count][1]}'>{list_deals[count][3]}</a>\n<b>Покупатель:</b> <a href='tg://user?id={list_deals[count][2]}'>{list_deals[count][4]}</a>\n\n"
                deals += f"<b>Сумма: </b>{list_deals[count][6]}\n"
                deals += f"<b>Условия: </b>{list_deals[count][5]}\n"
                if(list_deals[count][7] == 0):
                    status += "Не принята"
                elif(list_deals[count][7] == 1):
                    status += "Принята, не оплачена"
                elif(list_deals[count][7] == 2):
                    status += "Оплачена"
                elif(list_deals[count][7] == 3):
                    status += "Товар передан покупателю"
                elif(list_deals[count][7] == 4):
                    status += "Ведётся спор"
                elif(list_deals[count][7] == 5):
                    status += "Завершена"
                deals += f"<b>Статус: </b>{status}"
                deals += "\n➖➖➖➖➖➖➖➖➖➖➖\n"
        
        #Если пользователей меньше 5, то нет кнопок далее/назад
        if len(list_deals) <= 7:
            pass
        #Если больше 5 и это 1 страница, то кнопка далее
        elif len(list_deals) > 7 and remover < 7:
            keyboard.add(
                InlineKeyboardButton(f"💎 ", callback_data="..."),
                InlineKeyboardButton("Далее 👉", callback_data=f"deal_swipe:{remover + 7}:{userid}"),
            )
        #Если последняя страница, то кнопка назад
        elif remover + 7 >= len(list_deals):
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"deal_swipe:{remover - 7}:{userid}"),
                InlineKeyboardButton(f"💎 ", callback_data="..."),
            )
        #Если есть ещё пользователи, то кнопки назад и далее
        else:
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"deal_swipe:{remover - 7}:{userid}"),
                InlineKeyboardButton(f"💎 ", callback_data="..."),
                InlineKeyboardButton("Далее 👉", callback_data=f"deal_swipe:{remover + 7}:{userid}"),
            )
    else:
        deals += f"<b>Сделок нет!</b>"
    keyboard.add(InlineKeyboardButton(f"👈Вернуться в профиль", callback_data=f"back_to_profile:{userid}"),)
    return deals, keyboard

#Вывод отзывов на юзера
async def feedback(userid, remover, my_userid):

    list_feed = await db.feedbacks(userid)
    feedback = "Отзывы на пользователя:\n\n"
    keyboard = InlineKeyboardMarkup()
    if (len(list_feed) != 0):
        if remover >= len(list_feed): remover -= 7
        for count, a in enumerate(range(remover, len(list_feed))):
            if count < 7:
                feedback += f"*Оценка:* {list_feed[count][3]}\n*Отзыв:* {list_feed[count][4]}"
                feedback += f"\n➖➖➖➖➖➖➖➖➖➖➖\n"
        
        #Если пользователей меньше 5, то нет кнопок далее/назад
        if len(list_feed) <= 7:
            pass
        #Если больше 5 и это 1 страница, то кнопка далее
        elif len(list_feed) > 7 and remover < 7:
            keyboard.add(
                InlineKeyboardButton("Далее 👉", callback_data=f"feed_swipe:{remover + 7}:{userid}:{my_userid}"),
            )
        #Если последняя страница, то кнопка назад
        elif remover + 7 >= len(list_feed):
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"feed_swipe:{remover - 7}:{userid}:{my_userid}"),
            )
        #Если есть ещё пользователи, то кнопки назад и далее
        else:
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"feed_swipe:{remover - 7}:{userid}:{my_userid}"),
                InlineKeyboardButton("Далее 👉", callback_data=f"feed_swipe:{remover + 7}:{userid}:{my_userid}"),
            )
    else:
        feedback += f"*У пользователя нет отзывов :(*"
    keyboard.add(InlineKeyboardButton(f"👈Вернуться", callback_data=f"back_to_user:{userid}:{my_userid}"),)
    return feedback, keyboard

#Вывод споров юзера
async def my_disputes(userid, remover, status):

    list_disputes = await db.my_disputes(userid, status)
    keyboard = InlineKeyboardMarkup()

    if (len(list_disputes) != 0):
        if remover >= len(list_disputes): remover -= 7
        for count, a in enumerate(range(remover, len(list_disputes))):
            if (list_disputes[count][1] == "seller"):
                from_user = "Продавцом"
            elif (list_disputes[count][1] == "buyer"):
                from_user = "Покупателем"
            if count < 7:
                keyboard.add(InlineKeyboardButton(f"Сделка №{list_disputes[count][6]} | Создан: {from_user}", callback_data=f"my_disp_open:{userid}:{list_disputes[count][6]}"),)
        
        #Если пользователей меньше 5, то нет кнопок далее/назад
        if len(list_disputes) <= 7:
            pass
        #Если больше 5 и это 1 страница, то кнопка далее
        elif len(list_disputes) > 7 and remover < 7:
            keyboard.add(
                InlineKeyboardButton("Далее 👉", callback_data=f"disp_swipe:{remover + 7}:{userid}:{status}"),
            )
        #Если последняя страница, то кнопка назад
        elif remover + 7 >= len(list_disputes):
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"disp_swipe:{remover - 7}:{userid}:{status}"),
            )
        #Если есть ещё пользователи, то кнопки назад и далее
        else:
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"disp_swipe:{remover - 7}:{userid}:{status}"),
                InlineKeyboardButton("Далее 👉", callback_data=f"disp_swipe:{remover + 7}:{userid}:{status}"),
            )
    else:
         keyboard.add(InlineKeyboardButton(f"Споров нет :)", callback_data=f"..."),)
    keyboard.add(InlineKeyboardButton(f"👈 Вернуться", callback_data=f"my_disputes:{userid}"),)
    return keyboard

#Вывод сообщений в споре
async def my_disp_open(deal_id, remover, userid):

    list_disputes = await db.my_disputes_msg(deal_id)
    keyboard = InlineKeyboardMarkup()
    msg = "Сообщения.\n*Предоставляйте доказательства в виде ссылки на ваш скриншот!*\n\n"

    if (len(list_disputes) != 0):
        if remover >= len(list_disputes): remover -= 7
        for count, a in enumerate(range(remover, len(list_disputes))):
            if count < 7:
                if (list_disputes[count][1] == "seller"):
                    msg_from = "Продавца"
                elif (list_disputes[count][1] == "buyer"):
                    msg_from = "Покупателя"
                elif (list_disputes[count][1] == "admin"):
                    msg_from = "❗️Администратора❗️"

                msg += f"*От:* {msg_from}\n*Сообщение:* {list_disputes[count][2]}"
                msg += f"\n➖➖➖➖➖➖➖➖➖➖➖\n"
        
        #Если пользователей меньше 5, то нет кнопок далее/назад
        if len(list_disputes) <= 7:
            pass
        #Если больше 5 и это 1 страница, то кнопка далее
        elif len(list_disputes) > 7 and remover < 7:
            keyboard.add(
                InlineKeyboardButton("Далее 👉", callback_data=f"dispute_swipe:{remover + 7}:{deal_id}:{userid}"),
            )
        #Если последняя страница, то кнопка назад
        elif remover + 7 >= len(list_disputes):
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"dispute_swipe:{remover - 7}:{deal_id}:{userid}"),
            )
        #Если есть ещё пользователи, то кнопки назад и далее
        else:
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"dispute_swipe:{remover - 7}:{deal_id}:{userid}"),
                InlineKeyboardButton("Далее 👉", callback_data=f"dispute_swipe:{remover + 7}:{deal_id}:{userid}"),
            )
    else:
         msg += "Сообщений нет"
    disp = await db.check_disp(deal_id)
    if (disp[0][8] == 0):
        keyboard.add(InlineKeyboardButton(f"Добавить сообщение", callback_data=f"disp_add_msg:{deal_id}:{userid}"),)
    keyboard.add(InlineKeyboardButton(f"👈 Вернуться", callback_data=f"my_disputes:{userid}"),)
    return msg, keyboard

#Вывод заявок на вывод средств
async def my_payouts(userid, remover, status):

    list_feed = await db.my_payouts(userid, status)
    feedback = "Заявки на вывод:\n\n"
    keyboard = InlineKeyboardMarkup()
    if (len(list_feed) != 0):
        if remover >= len(list_feed): remover -= 7
        for count, a in enumerate(range(remover, len(list_feed))):
            if count < 7:
                feedback += f"*Заявка №{list_feed[count][0]}*\n*Сумма:* {list_feed[count][3]}"
                feedback += f"\n➖➖➖➖➖➖➖➖➖➖➖\n"
        
        #Если пользователей меньше 5, то нет кнопок далее/назад
        if len(list_feed) <= 7:
            pass
        #Если больше 5 и это 1 страница, то кнопка далее
        elif len(list_feed) > 7 and remover < 7:
            keyboard.add(
                InlineKeyboardButton("Далее 👉", callback_data=f"payouts_swipe:{remover + 7}:{userid}:{status}"),
            )
        #Если последняя страница, то кнопка назад
        elif remover + 7 >= len(list_feed):
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"feed_swipe:{remover - 7}:{userid}:{status}"),
            )
        #Если есть ещё пользователи, то кнопки назад и далее
        else:
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"feed_swipe:{remover - 7}:{userid}:{status}"),
                InlineKeyboardButton("Далее 👉", callback_data=f"feed_swipe:{remover + 7}:{userid}:{status}"),
            )
    else:
        feedback += f"*Нет заявок*"
    keyboard.add(InlineKeyboardButton(f"👈Вернуться", callback_data=f"my_payouts:{userid}"),)
    return feedback, keyboard