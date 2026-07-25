# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message

from tgbot.config import CURRENCY
from tgbot.keyboards.admin.main import close_this
from tgbot.keyboards.z_all_inline import back_search, choose_phone, choose_snils, choose_avto, not_money

from tgbot.services.api_sqlite import get_prices
from tgbot.utils.misc.bot_models import UserDB, FSM
from tgbot.utils.misc_functions import send_user_request
from tgbot.utils.states import SearchAvto

router_avto = Router()


@router_avto.callback_query(Text(text='choose_avto'))
async def choose_search_snils(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['avto'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        rm = not_money()
    else:
        bal_txt = ""
        rm = choose_avto()
    text = f"Стоимость запроса составляет {price} {CURRENCY}. " \
           f"Списание будет сделано сразу после выдачи отчёта.\n\n{bal_txt}"
    await call.message.edit_text(text=text, reply_markup=rm)


@router_avto.callback_query(Text(text='start_search_avto'))
async def search_choose_avto(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['avto'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        await call.answer(bal_txt)
        return
    await state.set_state(SearchAvto.number)
    await state.update_data(type_request="avto")
    text = "Отправьте номер авто (в формате: A777AA77 кирилицей)"
    await call.message.answer(text=text, reply_markup=close_this)


@router_avto.message(SearchAvto.number, F.text)
async def yearavto(message: Message, bot: Bot, state: FSM, user: UserDB):
    await state.update_data(avto=message.text)
    data = await state.get_data()
    await state.clear()
    await send_user_request(bot, user.user_id, data)



@router_avto.message(SearchAvto.number)
async def err_avto(message: Message):
    await message.answer('Некорректный ввод, поторите попытку ')