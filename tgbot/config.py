# - *- coding: utf- 8 - *-
import configparser
from environs import Env

from apscheduler.schedulers.asyncio import AsyncIOScheduler

env = Env()
env.read_env()

BOT_TOKEN = env.str("token")
ADMINS =[int(i) for i in env.list("ADMINS")]

CURRENCY = env.str("CURRENCY")
HIMERA_KEY = env.str("HIMERA_KEY")
scheduler = AsyncIOScheduler(timezone="Europe/Kiev")

PATH_DATABASE = "tgbot/data/database.db"  # Путь к БД
PATH_LOGS = "tgbot/data/logs.log"  # Путь к Логам


API_KEY_TRON = env.str("API_KEY_TRON")
MAIN_NET_TRON = env.str("MAIN_NET_TRON")

ADDRESS_USDT_TRC20 = env.str("ADDRESS_USDT_TRC20")
PK_USDT_TRC20 = env.str('PK_ADDRESS_USDT_TRC20')
ADDRESS_BNB= env.str("ADDRESS_BNB")
PK_BNB = env.str('PK_ADDRESS_BNB')

ADMIN_ANSWER_GROUP= env.int('Admin_answer')
TOKEN_QIWI= env.str('TOKEN_QIWI')
PHONE= env.str('PHONE')

m_id= env.int('m_id')
m_secret_1= env.str('m_secret_1')
m_secret_2= env.str('m_secret_2')