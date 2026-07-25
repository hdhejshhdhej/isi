# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from aiogram.types import Message

from tgbot.config import ADMINS
from tgbot.utils.misc.bot_models import UserDB, FSM
from tgbot.services.api_sqlite import new_ballance_user
from tgbot.keyboards.z_all_inline import back_withdraw_keyboard, back_amount_withdraw_keyboard, withdraw_keyboard
from tgbot.utils.create_wallet import check_payments
from tgbot.utils.states import Withdraw
from tgbot.utils.const_functions import is_number

from tgbot.utils.send_token import send_tokens
from tgbot.utils.token_to_dollar import get_rub_in_dollars, get_dollars_in_rub
from tgbot.utils.usdt_trc20 import NodeTron

router_withdraw = Router()


@router_withdraw.callback_query(Text(text='withdraw'))
async def withdraw_handler(call: CallbackQuery, state: FSM):
    await state.clear()
    await call.message.edit_text("<b>👇 Вывести</b>\n\n"
                                 "📋 Выберите нужную криптовалюту для вывода:",
                                 reply_markup=withdraw_keyboard())
    await call.answer()


@router_withdraw.callback_query(F.data.startswith('withdraw;'))
async def make_withdraw_handler(call: CallbackQuery, state: FSM, user: UserDB):
    await state.clear()
    cms = 2
    token = call.data.split(';')[1]

    ballance = await get_rub_in_dollars(user.ballance)
    print(ballance)

    if token == "BUSD" or token == "USDT_BEP20":
        token_ballance = await check_payments(token, "0xC594EbE6441b991D1C46548556F5905a681B859C", )
    else:
        token_ballance = await check_payments(token, "TKWTb9eaJxBBfmq9KcuBPc5T8QkGfK8zdY", )
    if ballance and ballance >= 12:
        if ballance > token_ballance:
            ballance = token_ballance + cms
        await call.message.edit_text(f"<b>👇 Вывести {token}</b>\n\n"
                                     f"Комиссия за вывод: {cms} {token}\n"
                                     f"👉 Введите сумму для вывода от 10 до {(ballance - cms):.2f}:",
                                     reply_markup=back_withdraw_keyboard)
        await state.set_state(Withdraw.amount)
        await state.update_data(token=token, max_amount=ballance - cms)

    else:
        await call.answer(f"У вас недостаточно на счету для вывода.\n\n"
                          f"Минимальная сумма вывода 10 {token}\n"
                          f"Комиссия на вывод: {cms} {token}", show_alert=True)


@router_withdraw.message(Withdraw.amount, F.text)
async def summa_withdraw_handler(message: Message, state: FSM, user: UserDB):
    amount = message.text.replace(",", ".")
    data = await state.get_data()
    if is_number(amount) and float(amount) <= data['max_amount'] and float(amount) >= 10:
        data = await state.update_data(amount=amount)
        await message.answer(f"<b>👇 Вывести {amount} {data['token']}</b>\n\n"
                             f"👉 Введите адрес для вывода:",
                             reply_markup=await back_amount_withdraw_keyboard())
        await state.set_state(Withdraw.adress)


    else:
        await message.answer(f"<b>👇 Вывести {data['token']}</b>\n\n"
                             "<b>Ошибка:</b> некорректные данные.\n\n"
                             f"👉 Введите сумму для вывода от 10 до {data['max_amount']}:",
                             reply_markup=await back_amount_withdraw_keyboard())


@router_withdraw.message(Withdraw.amount)
async def summa_withdraw_handler(message: Message, state: FSM, user: UserDB):
    data = await state.get_data()
    await message.answer(f"<b>👇 Вывести {data['token']}</b>\n\n"
                         "<b>Ошибка:</b> некорректные данные.\n\n"
                         f"👉 Введите сумму для вывода до {data['max_amount']}:",
                         reply_markup=await back_amount_withdraw_keyboard())


@router_withdraw.message(Withdraw.adress, F.text)
async def adress_withdraw_handler(message: Message, state: FSM, user: UserDB, bot: Bot):
    data = await state.get_data()
    if data['token'] == "USDT_TRC20":
        node = NodeTron()
        if not node.is_valid(message.text):
            await message.answer('Нужно ввести адрес USDT TRC20', reply_markup=back_withdraw_keyboard)
            return
    await state.clear()
    tx = await send_tokens(from_address=None,
                           from_private_key=None,
                           to_address=message.text,
                           token=data['token'],
                           amount=data['amount'])

    if len(tx) == 2 and tx[0] == 'error':
        text = 'Что-то пошло не так. Проверьте правильность введеных реквизитов или повторите попытку позднее'
        await message.answer(text)
        try:
            await bot.send_message(ADMINS[0], f"ошибка вывода {data['token']} c основного адресс \n\n"
                                              f"Пользователь {message.chat.username}\n"
                                              f"Cумма {data['amount']} {data['token']} "
                                              f"\n Адрес {message.text}\n"
                                              f"Ошибка  {tx[1]}")
        except:
            pass
        return
    cms = 2
    new_ballance_user(user_id=int(message.from_user.id), amout=-( get_dollars_in_rub(float(data['amount']) + cms)))
    await message.answer(f"✅ Вы успешно вывели {data['amount']} {data['token']} на адрес <code>{message.text}</code>"
                         f"\n\n Детали транзакции : {tx}")
    await bot.send_message(ADMINS[0], f"вывод {data['amount']}  {data['token']} \n\n"
                                      f"Кошелек {message.text}\n"
                                      f"Пользователь {message.chat.username}\n"
                                      f"User_ID {user.user_id} ")

