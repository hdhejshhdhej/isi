# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message

from tgbot.config import CURRENCY
from tgbot.keyboards.admin.main import close_this
from tgbot.keyboards.z_all_inline import back_search, choose_search_scoring, not_money

from tgbot.services.api_sqlite import get_prices
from tgbot.utils.misc.bot_models import UserDB, FSM
from tgbot.utils.misc_functions import send_user_request
from tgbot.utils.states import SearchScoring

router_scoring = Router()


@router_scoring.callback_query(Text(text='choose_scoring'))
async def start_search_scoring(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['scoring'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        rm = not_money()
    else:
        bal_txt = ""
        rm = choose_search_scoring()
    text = f"Стоимость запроса составляет {price} {CURRENCY}. " \
           f"Списание будет сделано сразу после выдачи отчёта.\n\n{bal_txt}"
    await call.message.edit_text(text=text, reply_markup=rm)


@router_scoring.callback_query(Text(text='start_search_scoring'))
async def search_people_scoring(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['scoring'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        await call.answer(bal_txt)
        return
    await state.set_state(SearchScoring.lastname)
    await state.update_data(type_request="scoring")
    text = "Отправьте фамилию"
    await call.message.answer(text=text, reply_markup=close_this)


@router_scoring.message(SearchScoring.lastname, F.text)
async def lastname_scoring(message: Message, state: FSM, user: UserDB):
    await state.update_data(lastname=message.text)
    text = "Отправьте имя"
    await message.answer(text=text, reply_markup=close_this)
    await state.set_state(SearchScoring.firstname)


@router_scoring.message(SearchScoring.firstname, F.text)
async def firstname_scoring(message: Message, state: FSM, user: UserDB):
    await state.update_data(firstname=message.text)
    text = "Отправьте отчество"
    await message.answer(text=text, reply_markup=close_this)
    await state.set_state(SearchScoring.middlename)


@router_scoring.message(SearchScoring.middlename, F.text)
async def middlename_scoring(message: Message, state: FSM, user: UserDB):
    await state.update_data(middlename=message.text)
    text = "Отправьте день рождения <i>(в формате: 01.01.1900 )</i>"
    await message.answer(text=text, reply_markup=close_this)
    await state.set_state(SearchScoring.birthday)


@router_scoring.message(SearchScoring.birthday, F.text.regexp('^[0-9]{1,2}\\.[0-9]{1,2}\\.[0-9]{4}$'))
async def day_scoring(message: Message, state: FSM, bot: Bot, user: UserDB):
    await state.update_data(birthday=message.text)
    data = await state.get_data()
    await state.clear()
    await send_user_request(bot, user.user_id, data)


@router_scoring.message(SearchScoring.lastname)
@router_scoring.message(SearchScoring.firstname)
@router_scoring.message(SearchScoring.middlename)
@router_scoring.message(SearchScoring.birthday)
async def err_scoring(message: Message):
    await message.answer('Некорректный ввод, поторите попытку ')
