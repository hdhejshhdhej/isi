# - *- coding: utf- 8 - *-
import os

from aiogram import Router, Bot, F  # <--- ДОБАВИЛ F
from aiogram.types import Message, FSInputFile

from tgbot.config import CURRENCY
from tgbot.keyboards.z_all_inline import search_main, my_wallet, my_history
from tgbot.keyboards.z_all_reply import user_menu
from tgbot.services.api_sqlite import get_prices
from tgbot.utils.const_functions import get_date
from tgbot.utils.misc.bot_models import UserDB, FSM, RS
from tgbot.utils.token_to_dollar import get_rub_course

router_user_menu = Router()


@router_user_menu.message(F.text == "🔍 Поиск")
async def menu_exchange_handler(message: Message, bot: Bot, state: FSM, rSession: RS, user: UserDB):
    await state.clear()
    await message.answer("Выберите тип поиска:", reply_markup=search_main())


@router_user_menu.message(F.text == "📊 Тарифы")
async def f1(message: Message, bot: Bot, state: FSM, user: UserDB):
    await state.clear()

    price = get_prices()
    text = f"<b>Запрос по фио (расширенный): {price['name_full']} {CURRENCY}</b>\n" \
           f"<b>Запрос по фио (стандарт):  {price['name_standart']} {CURRENCY}</b>\n" \
           f"<b>Запрос по телефону:  {price['phone']} {CURRENCY}</b>\n" \
           f"<b>Запрос по юр.лицу ИНН/ОГРН:  {price['inn']} {CURRENCY}</b>\n" \
           f"<b>Запрос по email:  {price['email']} {CURRENCY}</b>\n" \
           f"<b>Запрос по ИНН физ.лица:  {price['inn_fl']} {CURRENCY}</b>\n" \
           f"<b>Запрос по номеру паспорта:  {price['passport']} {CURRENCY}</b>\n" \
           f"<b>Запрос по СНИЛС:  {price['snils']} {CURRENCY}</b>\n" \
           f"<b>Запрос по номеру авто:  {price['avto']} {CURRENCY}</b>\n" \
           f"<b>Запрос по VIN:  {price['vin']} {CURRENCY}</b>\n" \
           f"<b>Скоринг запрос:  {price['scoring']} {CURRENCY}</b>\n"
    await message.answer(text=text, reply_markup=user_menu())


@router_user_menu.message(F.text == "🏦 Кошелек")
async def wallet_handler(message: Message, bot: Bot, state: FSM, rSession: RS, user: UserDB):
    await state.clear()
    text = f"<b>Ваш ID:  <code>{user.user_id} </code>\n" \
           f"Баланс: " \
           f"<code>{user.ballance:.2f} </code> {CURRENCY} </b>\n"
    await message.answer(text, reply_markup=my_wallet)


@router_user_menu.message(F.text == "🧍История запросов")
async def menu_exchange_handler(message: Message, bot: Bot, state: FSM, rSession: RS, user: UserDB):
    await state.clear()
    await message.answer("Выберите тип поиска, для просмотра истории запросов", reply_markup=my_history())
