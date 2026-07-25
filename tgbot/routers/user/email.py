# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message

from tgbot.config import CURRENCY
from tgbot.keyboards.admin.main import close_this
from tgbot.keyboards.z_all_inline import back_search, choose_phone, choose_email_kb, not_money

from tgbot.services.api_sqlite import get_prices
from tgbot.utils.misc.bot_models import UserDB, FSM
from tgbot.utils.misc_functions import send_user_request
from tgbot.utils.states import SearchEmail

router_email = Router()


@router_email.callback_query(Text(text='choose_email'))
async def choose_search_phone(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['email'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        rm = not_money()
    else:
        bal_txt = ""
        rm = choose_email_kb()
    text = f"Стоимость запроса составляет {price} {CURRENCY}. " \
           f"Списание будет сделано сразу после выдачи отчёта.\n\n{bal_txt}"
    await call.message.edit_text(text=text, reply_markup=rm)


@router_email.callback_query(Text(text='start_search_email'))
async def search_phone(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['email'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        await call.answer(bal_txt)
        return
    await state.set_state(SearchEmail.address)
    await state.update_data(type_request="email")
    text = "Отправьте email"
    await call.message.answer(text=text, reply_markup=close_this)


@router_email.message(SearchEmail.address,  F.text.regexp('^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$'))
async def year_stndart(message: Message, bot: Bot, state: FSM, user: UserDB):
    await state.update_data(email=message.text)
    data = await state.get_data()
    await state.clear()
    await send_user_request(bot, user.user_id, data)



@router_email.message(SearchEmail.address)
async def err_standart(message: Message):
    await message.answer('Некорректный ввод, поторите попытку ')