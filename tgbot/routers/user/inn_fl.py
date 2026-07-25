# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message

from tgbot.config import CURRENCY
from tgbot.keyboards.admin.main import close_this
from tgbot.keyboards.z_all_inline import back_search, choose_phone, choose_inn_fl, not_money

from tgbot.services.api_sqlite import get_prices
from tgbot.utils.misc.bot_models import UserDB, FSM
from tgbot.utils.misc_functions import send_user_request
from tgbot.utils.states import SearchINN

router_inn_fl = Router()


@router_inn_fl.callback_query(F.data == 'choose_inn_fl')
async def choose_search_inn_fl(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['inn_fl'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        rm = not_money()
    else:
        bal_txt = ""
        rm = choose_inn_fl()
    text = f"Стоимость запроса составляет {price} {CURRENCY}. " \
           f"Списание будет сделано сразу после выдачи отчёта.\n\n{bal_txt}"
    await call.message.edit_text(text=text, reply_markup=rm)


@router_inn_fl.callback_query(F.data == 'start_search_inn_fl')
async def search_inn_fl(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['inn_fl'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        await call.answer(bal_txt)
        return
    await state.set_state(SearchINN.number)
    await state.update_data(type_request="inn_fl")
    text = "Отправьте номер ИНН"
    await call.message.answer(text=text, reply_markup=close_this)


@router_inn_fl.message(SearchINN.number, F.text)
async def year_inn_fl(message: Message, bot: Bot, state: FSM, user: UserDB):
    if message.text.isdigit():
        await state.update_data( inn_fl=message.text)
        data = await state.get_data()
        await state.clear()
        await send_user_request(bot, user.user_id, data)
    else:
        await message.answer('Некорректный ввод, поторите попытку ')


@router_inn_fl.message(SearchINN.number)
async def err_inn_fl(message: Message):
    await message.answer('Некорректный ввод, поторите попытку ')
