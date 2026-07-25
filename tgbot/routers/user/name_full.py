# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message

from tgbot.config import CURRENCY
from tgbot.keyboards.admin.main import close_this
from tgbot.keyboards.z_all_inline import choose_search_people_kb, search_main, choose_search_people_kb_back, \
    choose_search_people_kb_standart, choose_search_name_full, not_money

from tgbot.services.api_sqlite import get_prices
from tgbot.utils.misc.bot_models import UserDB, FSM
from tgbot.utils.misc_functions import request_himera, send_admins, send_user_request
from tgbot.utils.states import  SearchNameFull

router_name_full = Router()


@router_name_full.callback_query(F.data == 'name_full')
async def start_search_name_full(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['name_full'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        rm = choose_search_people_kb_back()
    else:
        bal_txt = ""
        rm = choose_search_name_full()
    text = f"Стоимость запроса составляет {price} {CURRENCY}. " \
           f"Списание будет сделано сразу после выдачи отчёта.\n\n{bal_txt}"
    await call.message.edit_text(text=text, reply_markup=rm)


@router_name_full.callback_query(F.data == 'start_search_name_full')
async def search_people_name_full(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['name_full'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        await call.answer(bal_txt)
        return
    await state.set_state(SearchNameFull.lastname)
    await state.update_data(type_request="name_full")
    text = "Отправьте фамилию"
    await call.message.answer(text=text, reply_markup=close_this)


@router_name_full.message(SearchNameFull.lastname, F.text)
async def lastname_name_full(message: Message, state: FSM, user: UserDB):
    await state.update_data(lastname=message.text)
    text = "Отправьте имя"
    await message.answer(text=text, reply_markup=close_this)
    await state.set_state(SearchNameFull.firstname)


@router_name_full.message(SearchNameFull.firstname, F.text)
async def firstname_name_full(message: Message, state: FSM, user: UserDB):
    await state.update_data(firstname=message.text)
    text = "Отправьте отчество"
    await message.answer(text=text, reply_markup=close_this)
    await state.set_state(SearchNameFull.middlename)

@router_name_full.message(SearchNameFull.middlename, F.text)
async def middlename_name_full(message: Message, state: FSM, user: UserDB):
    await state.update_data(middlename=message.text)
    text = "Отправьте день рождения <i>(в формате: 01.01.1900 )</i>"
    await message.answer(text=text, reply_markup=close_this)
    await state.set_state(SearchNameFull.birthday)

@router_name_full.message(SearchNameFull.birthday, F.text.regexp('^[0-9]{1,2}\\.[0-9]{1,2}\\.[0-9]{4}$'))
async def day_name_full(message: Message, state: FSM, bot:Bot,user: UserDB):
    await state.update_data(birthday=message.text)
    data = await state.get_data()
    await state.clear()
    await send_user_request(bot, user.user_id, data)


@router_name_full.message(SearchNameFull.lastname)
@router_name_full.message(SearchNameFull.firstname)
@router_name_full.message(SearchNameFull.middlename)
@router_name_full.message(SearchNameFull.birthday)
async def err_name_full(message: Message):
    await message.answer('Некорректный ввод, поторите попытку ')
