# - *- coding: utf- 8 - *-
import sqlite3

from tgbot.config import PATH_DATABASE
from tgbot.utils.const_functions import get_unix, get_date


# Преобразование полученных данных в словарный вид
def dict_factory(cursor, row):
    d = {}

    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d

# Форматирование запроса без аргументов
def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())
# con.row_factory = sqlite3.Row

####################################################################################################
##################################### ФОРМАТИРОВАНИЕ ЗАПРОСОВ ######################################
# Форматирование запросов с аргументами
def update_format_with_args(sql, parameters: dict):
    if "XXX" not in sql:
        sql += " XXX "

    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())


# Форматирование запросов без аргументов
def update_format(sql, parameters: dict):
    sql = f"{sql} WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())


####################################### ЗАПРОСЫ К БАЗЕ ДАННЫХ ######################################
####################################################################################################
# Добавление пользователя
def add_userx(user_id, user_name, first_name, last_name):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_users "
                    "(user_id, user_name, first_name, last_name,  user_date) "
                    "VALUES (?, ?,  ?, ?, ?)",
                    [user_id, user_name, first_name, last_name,  get_date()])
        con.commit()


# Получение пользователя
def get_userx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        sql, parameters = update_format(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


# Получение пользователей
def get_usersx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        sql, parameters = update_format(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Получение всех пользователей
def get_all_usersx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        return con.execute(sql).fetchall()

def new_ballance_user(user_id, amout):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.execute(f"UPDATE storage_users SET ballance = ballance + {amout} WHERE user_id = {user_id}")
        con.commit()

# Редактирование пользователя
def update_userx(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_users SET"
        sql, parameters = update_format_with_args(sql, kwargs)
        parameters.append(user_id)
        con.execute(sql + "WHERE user_id = ?", parameters)
        con.commit()


# Удаление пользователя
def delete_userx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_users"
        sql, parameters = update_format(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


def get_prices():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM price"
        return con.execute(sql).fetchone()
# Получение кщшельков
def get_wallets(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM wallets"
        sql, parameters = update_format(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


def update_wallets(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO wallets "
         "(user_id) "
         "VALUES ( ?)",
         [user_id, ])
        # con.execute("INSERT INTO wallets (user_id, ) VALUES (?)",   [user_id,])
        con.commit()

def write_new_wallets(user_id,**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE wallets SET"
        sql, parameters = update_format_with_args(sql, kwargs)
        parameters.append(user_id)
        con.execute(sql + "WHERE user_id = ?", parameters)
        con.commit()
#################### FAQ
def write_faq(name_button, description, ):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.row_factory = dict_factory
        con.execute("INSERT INTO faq (name_button, description) VALUES (?,?)", [name_button, description, ])
        con.commit()

def get_all_faq():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = con.execute("SELECT * FROM faq")
        return sql.fetchall()

def get_faq(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM faq"
        sql, parameters = update_format(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

def get_faqs(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM faq"
        sql, parameters = update_format(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

def update_faq(id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE faq SET"
        sql, parameters = update_format_with_args(sql, kwargs)
        parameters.append(id)
        con.execute(sql + "WHERE id = ?", parameters)
        con.commit()

def delete_faq(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM faq"
        sql, parameters = update_format(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()
################################################
# Получение платежных систем
def get_paymentx():
    with sqlite3.connect(PATH_DATABASE) as con:
        get_response = con.execute("SELECT * FROM storage_payment")
        get_response = get_response.fetchone()
    return get_response


# Изменение платежных систем
def update_paymentx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        sql = f"UPDATE storage_payment SET XXX "
        sql, parameters = update_format_with_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Добавление пополнения в БД
def add_refillx(user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.execute("INSERT INTO storage_refill "
                    "(user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix])
        con.commit()


# Получение пополнения
def get_refillx(what_select, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as db:
        sql = f"SELECT {what_select} FROM storage_refill WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
    return get_response



def write_data_request(user_id, type_request, data, answer):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO request_storage (user_id, type_request, data, answer) VALUES (?,?,?,?)", [user_id, type_request, data, answer ])
        con.commit()

def get_data_request(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM request_storage"
        sql, parameters = update_format(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


def add_qiwi_last(dates):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.execute("INSERT INTO qiwi_last "
                    "(dates ) "
                    "VALUES (?)",
                    [dates])
        con.commit()

def get_qiwi_last():
    with sqlite3.connect(PATH_DATABASE) as con:
        sql = "SELECT * FROM qiwi_last"
        return con.execute(sql).fetchone()[0]


def update_qiwi_last(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        sql = f"UPDATE qiwi_last SET XXX "
        sql, parameters = update_format_with_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


def write_recipient(user_id, amount,status):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO recipient (user_id, amount,status, create_date) VALUES (?,?,?,?) ", [user_id, amount,status, get_date() ])
        con.commit()

        sql = "SELECT MAX(id) FROM recipient"
        return con.execute(sql).fetchone()['MAX(id)']

def update_recipient(id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE recipient SET"
        sql, parameters = update_format_with_args(sql, kwargs)
        parameters.append(id)
        con.execute(sql + "WHERE id = ?", parameters)
        con.commit()

def get_recipient(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM recipient"
        sql, parameters = update_format(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

def get_data_new_payment():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = con.execute("SELECT * FROM users_manage_pay_data")
        return sql.fetchall()


def delete_data_payment(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM users_manage_pay_data"
        sql, parameters = update_format(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()
######################################## СОЗДАНИЕ БАЗЫ ДАННЫХ ######################################
# Создание всех таблиц для Базы Данных
def create_bdx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory

        # Таблица с хранением пользователей
        check_sql = con.execute("PRAGMA table_info(storage_users)").fetchall()
        check_create_users = [c for c in check_sql]
        if len(check_create_users) == 10:
            print("DB was found(1/1)")
        else:
            con.execute("CREATE TABLE storage_users("
                        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "user_id INTEGER,"
                        "user_name TEXT,"
                        "first_name TEXT, "
                        "last_name TEXT,"
                        "ballance FLOAT default 0,"
                        "feed_back TEXT,"
                        "message_thread INTEGER,"
                        "ban INTEGER default 0,"
                        "user_date TIMESTAMP)")
            print("DB was not found(1/1) | Creating...")
        con.commit()
        check_sql_wallets = con.execute("PRAGMA table_info(wallets)").fetchall()
        check_wallets = [c for c in check_sql_wallets]
        if len(check_wallets) == 6:
            # con.execute("ALTER TABLE wallets ADD COLUMN address_busd TEXT")
            # con.execute("ALTER TABLE wallets ADD COLUMN primary_key_busd TEXT")

            print("DB  wallets(2/5) was found")
        else:
            con.execute("CREATE TABLE wallets("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "user_id INTEGER, "
                        "address_busd TEXT, "
                        "primary_key_busd TEXT, "
                        "address_usdt_trc20 TEXT, "
                        "primary_key_usdt_trc20 TEXT)")
            print("DB was not found(1/1) | Creating table wallets")
            con.commit()
        check_sql = con.execute("PRAGMA table_info(faq)")
        check_sql = check_sql.fetchall()
        check_purchases = [c for c in check_sql]
        if len(check_purchases) == 4:
            print("DB purchases was found")
        else:
            con.execute("CREATE TABLE faq("
                        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "name_button TEXT, "
                        "description INTEGER,"
                        "is_show BOOL default FALSE )")
            print("DB purchases was not found | Creating...")
        check_sql = con.execute("PRAGMA table_info(storage_payment)")
        check_sql = check_sql.fetchall()
        check_create_payment = [c for c in check_sql]
        if len(check_create_payment) == 6:
            print("DB was found(2/8)")
        else:
            con.execute("CREATE TABLE storage_payment("
                        "qiwi_login TEXT, qiwi_token TEXT, "
                        "qiwi_private_key TEXT, qiwi_nickname TEXT, "
                        "way_payment TEXT, status TEXT)")
            con.execute("INSERT INTO storage_payment("
                        "qiwi_login, qiwi_token, "
                        "qiwi_private_key, qiwi_nickname, "
                        "way_payment, status) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        ["None", "None", "None", "None", "form", "False"])
            print("DB was not found(2/8) | Creating...")
        # Создание БД с хранением пополнений пользователей
        check_sql = con.execute("PRAGMA table_info(storage_refill)")
        check_sql = check_sql.fetchall()
        check_create_refill = [c for c in check_sql]
        if len(check_create_refill) == 10:
            print("DB was found(4/8)")
        else:
            con.execute("CREATE TABLE storage_refill("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "user_id INTEGER, user_login TEXT, "
                        "user_name TEXT, comment TEXT, "
                        "amount TEXT, receipt TEXT, "
                        "way_pay TEXT, dates TIMESTAMP, "
                        "dates_unix TEXT)")
            print("DB was not found(4/8) | Creating...")
        con.commit()
        # Создание БД с хранением пополнений пользователей
        check_sql = con.execute("PRAGMA table_info(qiwi_last)")
        check_sql = check_sql.fetchall()
        check_create_refill = [c for c in check_sql]
        if len(check_create_refill) == 1:
            print("DB was found(4/8)")
        else:
            con.execute("CREATE TABLE qiwi_last("
                        "dates TEXT default '0')")
            print("DB was not found(4/8) | Creating...")
        con.commit()



