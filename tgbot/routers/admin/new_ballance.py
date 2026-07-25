# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery

from tgbot.config import CURRENCY
from tgbot.keyboards.admin_inline import new_balance
from tgbot.keyboards.admin.main import back_admin_menu
from tgbot.services.api_sqlite import get_userx, new_ballance_user
from tgbot.utils.const_functions import is_number
from tgbot.utils.misc.bot_models import FSM
from tgbot.utils.states import NewBallance

router_new_ballance = Router()


# Изменено: Text -> F.text
@router_new_ballance.message(F.text == "Пополнить баланс")
async def new_ballans(message: Message, state: FSM, ):
    await state.clear()
    await message.answer("Отправьте ID пользователя или user_name", reply_markup=back_admin_menu)
    await state.set_state(NewBallance.user_id)


@router_new_ballance.message(NewBallance.user_id, F.text)
async def new_ballans(message: Message, state: FSM ):
    usr = get_userx(user_id=message.text)
    if usr is None:
        username = (message.text[1:]).lower() if message.text[0] == "@" else message.text.lower()
        usr = get_userx(user_name=username)

    if usr is not None:
        await message.answer("Отправьте сумму пополнения, сумма может быть отрицательной")
        await state.update_data(user_id=usr['user_id'], user_name=usr['user_name'], ballance=usr['ballance'])
        await state.set_state(NewBallance.amout)
    else:
        await message.answer("Некорректный ввод", reply_markup=back_admin_menu)


@router_new_ballance.message(NewBallance.user_id)
async def new_ballans(message: Message):
    await message.answer("Некорректный ввод", reply_markup=back_admin_menu)


@router_new_ballance.message(NewBallance.amout, F.text)
async def amout(message: Message, state: FSM):
    if is_number(message.text):
        amout = message.text.replace(',', '.')
        data = await state.get_data()
        await message.answer(f'Вы хотите пополнить баланс Пользователю на {amout} {CURRENCY}:\n'
                             f'ID: {data["user_id"]}\n'
                             f'User Name: {data["user_name"]}\n'
                             f'Текущий баланс пользователя: {data["ballance"]}',
                             reply_markup=new_balance(data["user_id"], amout))
        await state.clear()
    else:
        await message.answer("Некорректный ввод", reply_markup=back_admin_menu)


@router_new_ballance.message(NewBallance.amout)
async def amout(message: Message):
    await message.answer("Некорректный ввод", reply_markup=back_admin_menu)


@router_new_ballance.callback_query(F.data.startswith('new_ballance'))
async def amout(call: CallbackQuery, bot: Bot, state: FSM):
    await state.clear()
    user_id, amout = call.data.split(';')[1], call.data.split(';')[2]
    new_ballance_user(user_id=int(user_id), amout=float(amout))
    await call.message.edit_text('Готово')
    await bot.send_message(chat_id=int(user_id), text=f"Ваш баланс пополнен на {amout} {CURRENCY}")
    await call.answer()
