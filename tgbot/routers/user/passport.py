# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message

from tgbot.config import CURRENCY
from tgbot.keyboards.admin.main import close_this
from tgbot.keyboards.z_all_inline import back_search, choose__passport, not_money

from tgbot.services.api_sqlite import get_prices
from tgbot.utils.misc.bot_models import UserDB, FSM
from tgbot.utils.misc_functions import send_user_request
from tgbot.utils.states import SearchPassport

router_passport = Router()


@router_passport.callback_query(F.data == 'choose_passport')
async def choose_passport(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['passport'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        rm = not_money()
    else:
        bal_txt = ""
        rm = choose__passport()
    text = f"Стоимость запроса составляет {price} {CURRENCY}. " \
           f"Списание будет сделано сразу после выдачи отчёта.\n\n{bal_txt}"
    await call.message.edit_text(text=text, reply_markup=rm)


@router_passport.callback_query(F.data == 'start_search_passport')
async def search_passport(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['passport'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        await call.answer(bal_txt)
        return
    await state.set_state(SearchPassport.number)
    await state.update_data(type_request="passport")
    text = "Отправьте серию и номер паспорта без пробелов"
    await call.message.answer(text=text, reply_markup=close_this)


@router_passport.message(SearchPassport.number, F.text)
async def year_passport(message: Message, bot: Bot, state: FSM, user: UserDB):
    await state.update_data( passport=message.text)
    data = await state.get_data()
    await state.clear()
    await send_user_request(bot, user.user_id, data)


@router_passport.message(SearchPassport.number)
async def err_standart(message: Message):
    await message.answer('Некорректный ввод, поторите попытку ')
