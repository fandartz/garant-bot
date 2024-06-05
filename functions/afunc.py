from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import db

#Вывод списка админов
async def admins(remover):

    list_admins = await db.admins()
    keyboard = InlineKeyboardMarkup()

    if (len(list_admins) != 0):
        if remover >= len(list_admins): remover -= 7
        for count, a in enumerate(range(remover, len(list_admins))):
            if count < 7:
                keyboard.add(InlineKeyboardButton(f"{list_admins[count][2]}", callback_data=f"admin_open:{list_admins[count][1]}"),)
        
        #Если пользователей меньше 5, то нет кнопок далее/назад
        if len(list_admins) <= 7:
            pass
        #Если больше 5 и это 1 страница, то кнопка далее
        elif len(list_admins) > 7 and remover < 7:
            keyboard.add(
                InlineKeyboardButton("Далее 👉", callback_data=f"adm_swipe:{remover + 7}"),
            )
        #Если последняя страница, то кнопка назад
        elif remover + 7 >= len(list_admins):
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"adm_swipe:{remover - 7}"),
            )
        #Если есть ещё пользователи, то кнопки назад и далее
        else:
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"adm_swipe:{remover - 7}"),
                InlineKeyboardButton("Далее 👉", callback_data=f"adm_swipe:{remover + 7}"),
            )
    keyboard.add(InlineKeyboardButton(f"👈 Вернуться", callback_data=f"back_to_amenu"),)
    return keyboard

#Вывод списка споров
async def adisputes(remover):

    list_dispute = await db.adisputes()
    keyboard = InlineKeyboardMarkup()

    if (len(list_dispute) != 0):
        if remover >= len(list_dispute): remover -= 7
        for count, a in enumerate(range(remover, len(list_dispute))):
            if count < 7:
                sum = await db.deal(list_dispute[count][6])
                keyboard.add(InlineKeyboardButton(f"Сделка №{list_dispute[count][6]} | Сумма: {sum[6]}", callback_data=f"adisp_open:{list_dispute[count][6]}"),)
        
        #Если пользователей меньше 5, то нет кнопок далее/назад
        if len(list_dispute) <= 7:
            pass
        #Если больше 5 и это 1 страница, то кнопка далее
        elif len(list_dispute) > 7 and remover < 7:
            keyboard.add(
                InlineKeyboardButton("Далее 👉", callback_data=f"adisp_swipe:{remover + 7}"),
            )
        #Если последняя страница, то кнопка назад
        elif remover + 7 >= len(list_dispute):
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"adisp_swipe:{remover - 7}"),
            )
        #Если есть ещё пользователи, то кнопки назад и далее
        else:
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"adisp_swipe:{remover - 7}"),
                InlineKeyboardButton("Далее 👉", callback_data=f"adisp_swipe:{remover + 7}"),
            )
    keyboard.add(InlineKeyboardButton(f"👈 Вернуться", callback_data=f"back_to_amenu"),)
    return keyboard

#Вывод сообщений в споре
async def a_disp_open(deal_id, remover):

    list_disputes_msg = await db.my_disputes_msg(deal_id)
    keyboard = InlineKeyboardMarkup()
    msg = "Сообщения.\n\n"

    if (len(list_disputes_msg) != 0):
        if remover >= len(list_disputes_msg): remover -= 7
        for count, a in enumerate(range(remover, len(list_disputes_msg))):
            if count < 7:
                if (list_disputes_msg[count][1] == "seller"):
                    msg_from = "Продавца"
                elif (list_disputes_msg[count][1] == "buyer"):
                    msg_from = "Покупателя"
                elif (list_disputes_msg[count][1] == "admin"):
                    msg_from = "❗️Администратора❗️"

                msg += f"*От:* {msg_from}\n*Сообщение:* {list_disputes_msg[count][2]}"
                msg += f"\n➖➖➖➖➖➖➖➖➖➖➖\n"
        
        #Если пользователей меньше 5, то нет кнопок далее/назад
        if len(list_disputes_msg) <= 7:
            pass
        #Если больше 5 и это 1 страница, то кнопка далее
        elif len(list_disputes_msg) > 7 and remover < 7:
            keyboard.add(
                InlineKeyboardButton("Далее 👉", callback_data=f"adispute_swipe:{remover + 7}:{deal_id}"),
            )
        #Если последняя страница, то кнопка назад
        elif remover + 7 >= len(list_disputes_msg):
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"adispute_swipe:{remover - 7}:{deal_id}"),
            )
        #Если есть ещё пользователи, то кнопки назад и далее
        else:
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"adispute_swipe:{remover - 7}:{deal_id}"),
                InlineKeyboardButton("Далее 👉", callback_data=f"adispute_swipe:{remover + 7}:{deal_id}"),
            )
    else:
         msg += "Сообщений нет"
    keyboard.add(InlineKeyboardButton(f"Добавить сообщение", callback_data=f"adisp_add_msg:{deal_id}"),)
    keyboard.add(InlineKeyboardButton(f"Прав продавец", callback_data=f"disp_close:seller:{deal_id}"),InlineKeyboardButton(f"Прав покупатель", callback_data=f"disp_close:buyer:{deal_id}"))
    keyboard.add(InlineKeyboardButton(f"👈 Вернуться", callback_data=f"adisputes"),)
    return msg, keyboard

async def payouts(remover):

    list_payouts = await db.payouts()
    keyboard = InlineKeyboardMarkup()

    if (len(list_payouts) != 0):
        if remover >= len(list_payouts): remover -= 7
        for count, a in enumerate(range(remover, len(list_payouts))):
            if count < 7:
                keyboard.add(InlineKeyboardButton(f"Заявка №{list_payouts[count][0]} | Сумма: {list_payouts[count][3]}", callback_data=f"payouts_open:{list_payouts[count][0]}"),)
        
        #Если пользователей меньше 5, то нет кнопок далее/назад
        if len(list_payouts) <= 7:
            pass
        #Если больше 5 и это 1 страница, то кнопка далее
        elif len(list_payouts) > 7 and remover < 7:
            keyboard.add(
                InlineKeyboardButton("Далее 👉", callback_data=f"adm_swipe:{remover + 7}"),
            )
        #Если последняя страница, то кнопка назад
        elif remover + 7 >= len(list_payouts):
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"adm_swipe:{remover - 7}"),
            )
        #Если есть ещё пользователи, то кнопки назад и далее
        else:
            keyboard.add(
                InlineKeyboardButton("👈 Назад", callback_data=f"adm_swipe:{remover - 7}"),
                InlineKeyboardButton("Далее 👉", callback_data=f"adm_swipe:{remover + 7}"),
            )
    keyboard.add(InlineKeyboardButton(f"👈 Вернуться", callback_data=f"back_to_amenu"),)
    return keyboard