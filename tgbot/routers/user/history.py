# - *- coding: utf- 8 - *-
import json

from aiofiles import os
from aiogram import Router, Bot, F
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message, FSInputFile

from tgbot.config import CURRENCY
from tgbot.keyboards.admin.main import close_this
from tgbot.keyboards.z_all_inline import choose_search_people_kb, search_main, choose_search_people_kb_back, \
    choose_search_people_kb_standart, choose_search_name_full, pag_history, my_history

from tgbot.services.api_sqlite import get_prices, get_data_request
from tgbot.utils.const_functions import get_date
from tgbot.utils.misc.bot_models import UserDB, FSM
from tgbot.utils.misc_functions import request_himera, send_admins, send_user_request
from tgbot.utils.states import SearchNameFull

router_history = Router()


@router_history.callback_query(F.data.startswith('history'))
async def start_search_name_full(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    type_request = call.data.split(";")[1]
    data = get_data_request(user_id=user.user_id, type_request=type_request)
    cnt_req = len(data)
    if cnt_req == 0:
        text = "Нет истории по даному запросу"
        await call.answer(text)
        return
    def mykey(a):
        return a['id']
    data = sorted(data, key=mykey, reverse=True)[0]
    text = ""
    req = json.loads(data['data'].replace("'","\""))
    for i in req:
        text += f'{req[i]}\n'
    text+= f"\n 1 из {cnt_req}"
    id = data['id']
    kb = pag_history(0, cnt_req, id, type_request)
    await call.message.edit_text(text=text, reply_markup=kb)

@router_history.callback_query(Text(text="back_history"))
async def menu_back_history(call: CallbackQuery, bot: Bot, state: FSM,  user: UserDB):
    await state.clear()
    await call.message.edit_text("Выберите тип поиска, для просморта истории запросов", reply_markup=my_history())


@router_history.callback_query(F.data.startswith("prew"))
async def menu_prew(call: CallbackQuery, bot: Bot, state: FSM,  user: UserDB):
    await state.clear()
    d = call.data.split(';')
    type_request, total_index = d[1], int(d[2])
    data = get_data_request(user_id=user.user_id, type_request=type_request)
    cnt_req = len(data)
    if total_index == 0:
        total_index = cnt_req-1
    else:
        total_index = int(total_index) - 1

    def mykey(a):
        return a['id']
    data = sorted(data, key=mykey, reverse=True)[total_index]
    text = ""
    req = json.loads(data['data'].replace("'","\""))
    for i in req:
        text += f'{req[i]}\n'
    text+= f"\n {int(total_index)+1} из {cnt_req}"
    id = data['id']
    kb = pag_history(total_index, cnt_req, id, type_request)
    await call.message.edit_text(text=text, reply_markup=kb)

@router_history.callback_query(F.data.startswith("next"))
async def menu_next(call: CallbackQuery, bot: Bot, state: FSM,  user: UserDB):
    await state.clear()
    d = call.data.split(';')
    type_request, total_index = d[1], int(d[2])
    data = get_data_request(user_id=user.user_id, type_request=type_request)
    cnt_req = len(data)
    if total_index == cnt_req-1:
        total_index = 0
    else:
        total_index = int(total_index) + 1

    def mykey(a):
        return a['id']
    data = sorted(data, key=mykey, reverse=True)[total_index]
    text = ""
    req = json.loads(data['data'].replace("'","\""))
    for i in req:
        text += f'{req[i]}\n'
    text+= f"\n {int(total_index)+1} из {cnt_req}"
    id = data['id']
    kb = pag_history(total_index, cnt_req, id, type_request)
    await call.message.edit_text(text=text, reply_markup=kb)



@router_history.callback_query(F.data.startswith("download"))
async def menu_download(call: CallbackQuery, bot: Bot, state: FSM,  user: UserDB):
    await state.clear()
    baner = ''' 

Форум "Probiv" - https://up.probiv.in
Форум "Probiv" VPN  - https://probiv.one
Форум "Probiv Onion" - https://probiv7zf4357jpj7byfs72a3oa7g25hidbip7kpvpgcx2orolxsi4ad.onion\n\n
                '''

    data = get_data_request(user_id=user.user_id, id=int(call.data.split(";")[1]))
    text =data[0]['answer']
    date = get_date()
    with open(f"{date}.txt", "w") as file:
        file.write(baner + text)
    document = FSInputFile(f"{date}.txt")
    await bot.send_document(chat_id=user.user_id, document=document)
    await os.remove(f"{date}.txt")

