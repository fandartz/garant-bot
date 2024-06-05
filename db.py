import sqlite3 as sq

from datetime import datetime as dt

import main

db = sq.connect('db.db')
cur = db.cursor()

#Запуск и создание БД
async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "userid INTEGER,"
                "name TEXT,"
                "username TEXT,"
                "status TEXT,"
                "is_admin INTEGER,"
                "balance INTEGER,"
                "date INTEGER,"
                "sell INTEGER,"
                "buy INTEGER,"
                "sum_sell INTEGER,"
                "sum_buy INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS deals("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "seller_userid INTEGER,"
                "buyer_userid INTEGER,"
                "seller_name TEXT,"
                "buyer_name TEXT,"
                "description TEXT,"
                "sum INTEGER,"
                "status INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS feedback("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "userid INTEGER,"
                "from_userid INTEGER,"
                "type TEXT,"
                "description TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS dispute("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "from_user TEXT,"
                "seller_userid INTEGER,"
                "buyer_userid INTEGER,"
                "seller_name TEXT,"
                "buyer_name TEXT,"
                "deal_id INTEGER,"
                "desc TEXT,"
                "status INTEGER,"
                "winner INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS dispute_msg("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "from_user TEXT,"
                "message INTEGER,"
                "deal_id INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS payouts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "userid INTEGER,"
                "name TEXT,"
                "sum INTEGER,"
                "status INTEGER,"
                "bank TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS donate("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "userid INTEGER,"
                "name TEXT,"
                "sum INTEGER)")
    db.commit()
    
#добавление/обновление пользователя в БД
async def cmd_start_db(user_id, user_name, username, is_admin, status):
    user = cur.execute(f"SELECT * FROM accounts WHERE userid == {user_id}").fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (userid, name, username, status, is_admin, balance, date, sell, buy, sum_sell, sum_buy) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, f"{user_name}", f"{username.lower()}", f"{status}", is_admin, 0, int(dt.now().timestamp()), 0, 0, 0, 0,))
        db.commit()
    else:
        if (user_id == main.always_admin):
            cur.execute(f"UPDATE accounts SET username = '{username.lower()}', name = '{user_name}', is_admin = 1 WHERE userid == {user_id}")
        else:
            cur.execute(f"UPDATE accounts SET username = '{username.lower()}', name = '{user_name}' WHERE userid == {user_id}")
        db.commit()

#Проверка на админа
async def check_admin(user_id):
    user = cur.execute('SELECT is_admin FROM accounts WHERE userid = ?',(user_id,)).fetchone()[0]
    return user

#Вывод всех пользователей
async def users():
    users = cur.execute("SELECT * FROM accounts").fetchall()
    return users

#Вывод всех админов
async def admins():
    users = cur.execute("SELECT * FROM accounts WHERE is_admin == 1").fetchall()
    return users

#Инфа о профиле
async def profile(user_id):
    user = cur.execute(f"SELECT * FROM accounts WHERE userid == {user_id}").fetchone()
    return user

#Вывод моих сделок
async def mydeals(user_id):
    deals = cur.execute(f"SELECT * FROM deals WHERE seller_userid == {user_id} OR buyer_userid == {user_id}").fetchall()
    return deals

#Обновление инфы о юзере
async def upd_user(type, set, userid):
    cur.execute(f"UPDATE accounts SET {type} = {set} WHERE userid == {userid}")
    db.commit()

#Обновление инфы о админе
async def upd_user_adm(type, set, userid):
    cur.execute(f"UPDATE accounts SET {type} = '{set}' WHERE userid == {userid}")
    db.commit()

#Поиск пользователя
async def find_user(type, find):
    try:
        if (type == 'userid'):
            deals = cur.execute(f"SELECT * FROM accounts WHERE {type} == {int(find)}").fetchone()
            return deals
        elif (type == 'username'):
            deals = cur.execute(f"SELECT * FROM accounts WHERE {type} == '{find.lower()}'").fetchone()
            return deals
    except:
        text = "Произошла ошибка! Перепроверьте данные и попробуйте снова!"
        return text

#Вывод отзывов
async def feedbacks(userid):
    feed = cur.execute(f"SELECT * FROM feedback WHERE userid == {userid}").fetchall()
    return feed

#Добавление отзыва
async def add_feedback(userid, from_userid, type, description):
    cur.execute("INSERT INTO feedback (userid, from_userid, type, description) VALUES (?, ?, ?, ?);", (userid, from_userid, f"{type}", f"{description}",))
    db.commit()

#Добавление сделки
async def add_deal(seller_userid, buyer_userid, seller_name, buyer_name, desc, sum):
    cur.execute(f"INSERT INTO deals (seller_userid, buyer_userid, seller_name, buyer_name, description, sum, status) VALUES (?, ?, ?, ?, ?, ?, ?);", (seller_userid, buyer_userid, f"{seller_name}", f"{buyer_name}", f"{desc}", sum, 0,))
    db.commit()
    return cur.lastrowid

#Удаление сделки
async def del_deal(id):
    cur.execute(f"DELETE FROM deals WHERE id == {id}")
    db.commit()

#Поиск сделки
async def deal(id):
    deal = cur.execute(f"SELECT * FROM deals WHERE id == {id}").fetchone()
    return deal

#Вывод всех сделок
async def deals():
    deal = cur.execute(f"SELECT * FROM deals").fetchall()
    return deal

#Вывод суммы сделок
async def deals_sum():
    deal = cur.execute(f"SELECT SUM(sum) FROM deals").fetchone()
    return deal[0]

#Обновление сделки
async def upd_deal(id, status):
    cur.execute(f"UPDATE deals SET status = {status} WHERE id == {id}")
    db.commit()

#Проверка спора
async def check_disp(deal_id):
    disp = cur.execute(f"SELECT * FROM dispute WHERE deal_id == {deal_id}").fetchall()
    return disp

#Добавление спора
async def dispute_add(from_user, seller_userid, buyer_userid, seller_name, buyer_name, deal_id, desc):
    cur.execute(f"INSERT INTO dispute (from_user, seller_userid, buyer_userid, seller_name, buyer_name, deal_id, desc, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", (f"{from_user}", seller_userid, buyer_userid, f"{seller_name}", f"{buyer_name}", deal_id, f"{desc}", 0,))
    db.commit()

#Мои споры
async def my_disputes(userid, status):
    disputes = cur.execute(f"SELECT * FROM dispute WHERE seller_userid == {userid} OR buyer_userid == {userid} AND status == {status}").fetchall()
    return disputes

#Кол-во споров
async def disputes_count(userid):
    disputes = cur.execute(f"SELECT * FROM dispute WHERE seller_userid == {userid} OR buyer_userid == {userid}").fetchall()
    return disputes

#Кол-во выигранных споров
async def disputes_win(userid):
    disputes = cur.execute(f"SELECT * FROM dispute WHERE winner == {userid}").fetchall()
    return disputes

#Открытые споры для админов
async def adisputes():
    disputes = cur.execute(f"SELECT * FROM dispute WHERE status == 0").fetchall()
    return disputes

#Вывод сообщений у спора
async def my_disputes_msg(deal_id):
    disputes_msg = cur.execute(f"SELECT * FROM dispute_msg WHERE deal_id == {deal_id}").fetchall()
    return disputes_msg

#Добавление сообщений к спору
async def dispute_add_msg(from_user, msg, deal_id):
    cur.execute(f"INSERT INTO dispute_msg (from_user, message, deal_id) VALUES (?, ?, ?);", (f"{from_user}", f"{msg}", deal_id,))
    db.commit()

#Кто создал спор
async def dispute_from(deal_id):
    dispute = cur.execute(f"SELECT * FROM dispute WHERE deal_id == {deal_id}").fetchone()
    return dispute

#Завершение спора
async def dispute_update(deal_id, userid):
    cur.execute(f"UPDATE dispute SET status = 1 WHERE deal_id == {deal_id}")
    cur.execute(f"UPDATE dispute SET winner = {userid} WHERE deal_id == {deal_id}")
    db.commit()

#Мои заявки на вывод
async def my_payouts(userid, status):
    payouts = cur.execute(f"SELECT * FROM payouts WHERE userid == {userid} AND status == {status}").fetchall()
    return payouts

#Создание заявки
async def create_payout(userid, name, sum, bank):
    cur.execute(f"INSERT INTO payouts (userid, name, sum, status, bank) VALUES (?, ?, ?, ?, ?);", (userid, f"{name}", sum, 0, f"{bank}",))
    db.commit()

async def payouts():
    payouts = cur.execute(f"SELECT * FROM payouts WHERE status == 0").fetchall()
    return payouts

async def current_payout(id):
    payouts = cur.execute(f"SELECT * FROM payouts WHERE id == {id}").fetchone()
    return payouts

async def upd_payout(id):
    cur.execute(f"UPDATE payouts SET status = 1 WHERE id == {id}")
    db.commit()

async def del_payout(id):
    cur.execute(f"DELETE FROM payouts WHERE id == {id}")
    db.commit()

#Проверка на донат
async def check_donate(userid):
    donate = cur.execute(f"SELECT * FROM donate WHERE userid == {userid}").fetchone()
    return donate

#Обновление доната
async def upd_donate(userid, sum):
    cur.execute(f"UPDATE donate SET sum = {sum} WHERE userid == {userid}")
    db.commit()

#Создание доната
async def create_donate(userid, name, sum):
    cur.execute(f"INSERT INTO donate (userid, name, sum) VALUES (?, ?, ?);", (userid, f"{name}", sum,))
    db.commit()

#Топ донатеров
async def top_donate():
    payouts = cur.execute(f"SELECT * FROM donate ORDER BY sum DESC LIMIT 5;").fetchall()
    return payouts