# - *- coding: utf- 8 - *-
from hashlib import md5

from aiofiles import os
from aiogram import Bot
from aiogram.types import FSInputFile
from aiohttp import ClientSession
from tgbot.config import ADMINS, PATH_DATABASE, HIMERA_KEY, m_id, m_secret_1, m_secret_2
from tgbot.services.api_sqlite import get_prices, new_ballance_user, write_data_request, get_qiwi_last, get_userx, \
    update_qiwi_last, get_data_new_payment, get_recipient, delete_data_payment, update_recipient
from tgbot.utils.const_functions import get_date

# from qiwi_api import Qiwi

# api = Qiwi(TOKEN_QIWI)


# Выполнение функции после запуска бота (рассылка админам о запуске бота)
async def startup_notify(bot: Bot):
    if len(ADMINS) >= 1:
        await send_admins(bot, "<b>✅ Бот был запущен</b>")


# Автоматические бэкапы БД
async def autobackup(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_document(admin, FSInputFile(PATH_DATABASE),
                                    caption=f"<b>📦 AUTOBACKUP</b>\n"
                                            f"<code>🕰 {get_date()}</code>")
        except:
            pass


# Отправка сообщения всем админам
async def send_admins(bot: Bot, message, markup=None, not_me=0):
    for admin in ADMINS:
        try:
            if str(admin) != str(not_me):
                await bot.send_message(admin, message, reply_markup=markup, disable_web_page_preview=True)
        except:
            pass


async def request_himera(type_request, **kwargs):
    """The main request method for Payeer API"""
    data = {'key': HIMERA_KEY}
    api_url = 'https://api.himera-search.info/2.0/'
    if kwargs:
        data.update(kwargs)
    headers = {}
    async with ClientSession(headers=headers) as session:
        async with session.post(url=api_url + type_request, data=data, headers=headers) as r:
            resp = await r.json()
    error = resp.get('error')
    if error:
        return False, error
    return True, resp


async def send_user_request(bot: Bot, user_id, data):
    type_request = data['type_request']
    data.pop('type_request')
    r = await request_himera(type_request, **data)

    price = float(get_prices()[type_request])
    ballance = get_userx(user_id=user_id)['ballance']
    if ballance < price:
        return
    new_ballance_user(user_id, -price)
    if not r[0]:
        if r[1] == "invalid phone format":
            await bot.send_message(chat_id=user_id, text="invalid phone format")
            return
        await send_admins(bot, f'Рассылка админам\n\n Ошибка запроса {r[1]}')
        await bot.send_message(chat_id=user_id, text="Ведутся тех. работы повторите запрос позже")
        new_ballance_user(user_id, price)
        return
    if r[1]['status'] == "not_found" or r[1]['data'] == None:
        await bot.send_message(chat_id=user_id, text="По Вашему запросу ничего не найдено")
        new_ballance_user(user_id, price)
        return
    if r[1]['status'] == "ok":
        baner = ''' 
**********************************************************************
Другие  пробивы любой сложности  у наших селлеров на Форуме Probiv:
Бот форума - @ProbivLingk_bot
Без VPN - https://ru.probiv.fun
C VPN  - https://probiv.one
Onion - https://probiv7zf4357jpj7byfs72a3oa7g25hidbip7kpvpgcx2orolxsi4ad.onion
**********************************************************************
'''
        text = ""
        print(r)
        # for i in r[1]['data']:
        #     for j in i:
                
        #         text += f'{j} {i[j]}\n'
        #     text += "\n\n"
        
      
        if isinstance(r[1]['data'], list):
            for i in r[1]['data']:
                for j in i:
                    # print(j)
                    text += f'{j} {i[j]}\n'
                text += "\n\n"

        else:
            for k, v in r[1]['data'].items():
                if isinstance(v, list):
                    v = v[-1]
                for k,v in v.items():
                    text += f'{k} {v}\n'
                text += "\n\n"

        date = get_date()
        with open(f"{date}.txt", "w") as file:
            file.write(baner+text)
        document = FSInputFile(f"{date}.txt")
        await bot.send_document(chat_id=user_id, document=document)

        await os.remove(f"{date}.txt")
        write_data_request(user_id, type_request, str(data), text)
        await  bot.send_message(chat_id=user_id, text=baner+text[:3250] + "...")











def generate_link(amount, order_id):


    s = f"{m_id}|{m_secret_1}|{amount}|{order_id}"
    sign = md5(s.encode()).hexdigest()
    link = f"https://linepay.fun/pay?m_id={m_id}&amount={amount}&order_id={order_id}&sign={sign}"

    s_hash = f"{m_id}|{m_secret_2}|{amount}|{order_id}"
    hash_md5 = md5(s_hash.encode()).hexdigest()
    return link, hash_md5

async def new_balance_linepay(bot:Bot):
    new_payment = get_data_new_payment()
    for i in new_payment:
        hashmd5 = i['sign']
        amount = i['amount']
        print(hashmd5)
        recipient = get_recipient(hashmd5=hashmd5)
        print(recipient)
        if recipient:
            new_ballance_user(user_id=recipient['user_id'],amout=amount)
            text = f"Ваш баланс пополнен на {amount} р."
            await bot.send_message(chat_id=recipient['user_id'], text=text)
            delete_data_payment(id=i['id'])
            update_recipient(id=recipient['id'], status="Оплачено")