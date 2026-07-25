# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.config import CURRENCY
from tgbot.keyboards.admin.main import close_this
from tgbot.keyboards.z_all_inline import choose_search_people_kb, search_main, choose_search_people_kb_back, \
    choose_search_people_kb_standart, first_name_name_standart, name_name_name_standart, name_name_standart, \
    name_no_day, name_no_month, name_no_year

from tgbot.services.api_sqlite import get_prices, new_ballance_user
from tgbot.utils.misc.bot_models import UserDB, FSM
from tgbot.utils.misc_functions import request_himera, send_admins, send_user_request
from tgbot.utils.states import SearchNameStandart

router_people_data = Router()


@router_people_data.callback_query(Text(text="back_search"))
async def menu_exchange_handler(call: CallbackQuery, state: FSM):
    await state.clear()
    await call.message.answer("Выберите тип поиска:", reply_markup=search_main())
    await call.answer()


# @router_people_data.callback_query(Text(text='choose_search_people'))
# async def choose_search_people(call: CallbackQuery, state: FSM, ):
#     await state.clear()
#       await call.message.answer("Выберите тип поиска:", reply_markup=search_main())

#     await call.answer()




@router_people_data.callback_query(Text(text='choose_search_people'))
async def start_search_name_standart(call: CallbackQuery, state: FSM, user: UserDB):
    # new_ballance_user(user.user_id, 1000)
    await state.clear()
    price = float(get_prices()['name_standart'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        rm = choose_search_people_kb_back()
    else:
        bal_txt = ""
        rm = choose_search_people_kb_standart()
    text = f"Стоимость запроса составляет {price} {CURRENCY}. " \
           f"Списание будет сделано сразу после выдачи отчёта.\n\n{bal_txt}"
    await call.message.edit_text(text=text, reply_markup=rm)


#  Фамилия
@router_people_data.callback_query(Text(text='start_search_people_standart'))
async def search_people_standart(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    price = float(get_prices()['name_standart'])
    if price > user.ballance:
        bal_txt = " Недостаточно средств для выполнения запроса, пожалуйста пополните баланс"
        await call.answer(bal_txt)
        return
    await state.set_state(SearchNameStandart.lastname)
    await state.update_data(type_request="name_standart")
    text = "Отправьте фамилию"
    await call.message.answer(text=text, reply_markup=first_name_name_standart())


#  Пропустить Фамилию Указать имя
@router_people_data.callback_query(F.data.startswith("nxt_state_name"))
async def firstname_stndart_call(call: CallbackQuery, state: FSM, user: UserDB):
    text = "Отправьте имя"
    await call.message.answer(text=text, reply_markup=name_name_name_standart())
    await state.set_state(SearchNameStandart.firstname)
    await call.answer()
# Указать имя
@router_people_data.message(SearchNameStandart.lastname, F.text)
async def lastname_stndart(message: Message, state: FSM, user: UserDB):
    await state.update_data(lastname=message.text)
    text = "Отправьте имя"

    await message.answer(text=text, reply_markup=name_name_name_standart())
    await state.set_state(SearchNameStandart.firstname)


# # Пропустить имя указать отчество
@router_people_data.callback_query(F.data == "nxt_state_otcher")
async def firstname_stndart_call(call: CallbackQuery, state: FSM, user: UserDB):
    text = "Отправьте отчество"
    await call.message.answer(text=text, reply_markup=name_name_standart())
    await state.set_state(SearchNameStandart.middlename)

    await call.answer()
#  указать отчество
@router_people_data.message(SearchNameStandart.firstname, F.text)
async def firstname_stndart(message: Message, state: FSM, user: UserDB):
    await state.update_data(firstname=message.text)
    text = "Отправьте отчество"

    await message.answer(text=text, reply_markup=name_name_standart())
    await state.set_state(SearchNameStandart.middlename)


@router_people_data.callback_query(F.data.startswith("nxt_state"))
async def firstname_stndart_call(call: CallbackQuery, state: FSM, user: UserDB):
    text = "Отправьте день рождения <i>(целое число от 1 до 31)</i>"
    await call.message.answer(text=text, reply_markup=name_no_day())
    await state.set_state(SearchNameStandart.day)
    await call.answer()

@router_people_data.message(SearchNameStandart.middlename, F.text)
async def middlename_stndart(message: Message, state: FSM, user: UserDB):
    await state.update_data(middlename=message.text)
    text = "Отправьте день рождения <i>(целое число от 1 до 31)</i>"
    await message.answer(text=text, reply_markup=name_no_day())
    await state.set_state(SearchNameStandart.day)






@router_people_data.callback_query(F.data.startswith("name_no_day"))
async def firstname_stndart_call(call: CallbackQuery, state: FSM, user: UserDB):
    text = "Отправьте месяц  <i>(целое число от 1 до 12)</i>"
    await call.message.answer(text=text, reply_markup=name_no_month())
    await state.set_state(SearchNameStandart.day)
    await call.answer()

@router_people_data.message(SearchNameStandart.day, F.text)
async def day_stndart(message: Message, state: FSM, user: UserDB):
    if message.text.isdigit() and int(message.text) > 0 and int(message.text) < 32:
        day = message.text if len(message.text) == 2 else "0" + message.text
        await state.update_data(day=day)
        text = "Отправьте месяц  <i>(целое число от 1 до 12)</i>"
        await message.answer(text=text, reply_markup=name_no_month())
        await state.set_state(SearchNameStandart.mounth)
    else:
        await message.answer('Некорректный ввод, поторите попытку ')



@router_people_data.callback_query(F.data.startswith("name_no_month"))
async def firstname_stndart_call(call: CallbackQuery, state: FSM, user: UserDB):
    text = "Отправьте год рождения"
    await call.message.answer(text=text, reply_markup=name_no_year())
    await state.set_state(SearchNameStandart.year)

    await call.answer()


@router_people_data.message(SearchNameStandart.mounth, F.text)
async def mounth_stndart(message: Message, state: FSM, user: UserDB):
    if message.text.isdigit() and int(message.text) > 0 and int(message.text) < 13:
        mounth = message.text if len(message.text) == 2 else "0" + message.text
        await state.update_data(mounth=mounth)
        text = "Отправьте год рождения"
        await message.answer(text=text, reply_markup=name_no_year())
        await state.set_state(SearchNameStandart.year)
    else:
        await message.answer('Некорректный ввод, поторите попытку ')






@router_people_data.callback_query(F.data.startswith("name_no_year"))
async def fname_no_year( call: CallbackQuery, state: FSM, user: UserDB, bot:Bot):

    data = await state.get_data()
    await state.clear()
    if len(data) == 1:
        await call.answer("Вы не указали параметры для поиска")
    await send_user_request(bot, user.user_id, data)
    await call.answer()

@router_people_data.message(SearchNameStandart.year, F.text)
async def year_stndart(message: Message, bot: Bot, state: FSM, user: UserDB):
    if message.text.isdigit() and len(message.text) == 4:
        await state.update_data(year=message.text)
        data = await state.get_data()
        await state.clear()
        await send_user_request(bot, user.user_id, data)
    else:
        await message.answer('Некорректный ввод, поторите попытку ')


@router_people_data.message(SearchNameStandart.lastname)
@router_people_data.message(SearchNameStandart.firstname)
@router_people_data.message(SearchNameStandart.middlename)
async def err_standart(message: Message):
    await message.answer('Некорректный ввод, поторите попытку ')
