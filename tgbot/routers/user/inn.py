# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message

from tgbot.config import CURRENCY
from tgbot.keyboards.admin.main import close_this
from tgbot.keyboards.z_all_inline import back_search, choose_phone, choose_inn_fl, choose_inn, not_money

from tgbot.services.api_sqlite import get_prices
from tgbot.utils.misc.bot_models import UserDB, FSM
from tgbot.utils.misc_functions import send_user_request
from tgbot.utils.states import SearchINN_U

router_inn = Router()


@router_inn.callback_query(Text(text='choose_inn'))
async def choose_search_inn(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['inn'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        rm = not_money()
    else:
        bal_txt = ""
        rm = choose_inn()
    text = f"Стоимость запроса составляет {price} {CURRENCY}. " \
           f"Списание будет сделано сразу после выдачи отчёта.\n\n{bal_txt}"
    await call.message.edit_text(text=text, reply_markup=rm)


@router_inn.callback_query(Text(text='start_search_inn'))
async def search_inn_(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['inn'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        await call.answer(bal_txt)
        return
    await state.set_state(SearchINN_U.number)
    await state.update_data(type_request="inn_fl")
    text = "Отправьте номер ИНН"
    await call.message.answer(text=text, reply_markup=close_this)


@router_inn.message(SearchINN_U.number, F.text)
async def year_inn_(message: Message, bot: Bot, state: FSM, user: UserDB):
    if message.text.isdigit():
        await state.update_data( inn_fl=message.text)
        data = await state.get_data()
        await state.clear()
        await send_user_request(bot, user.user_id, data)
    else:
        await message.answer('Некорректный ввод, поторите попытку ')


@router_inn.message(SearchINN_U.number)
async def err_inn(message: Message):
    await message.answer('Некорректный ввод, поторите попытку ')