# - *- coding: utf- 8 - *-

from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.admin.main import close_this
from tgbot.keyboards.z_all_inline import pay_linepay

from tgbot.services.api_sqlite import write_recipient, update_recipient
from tgbot.utils.const_functions import is_number

from tgbot.utils.misc.bot_models import UserDB, FSM, RS
from tgbot.utils.misc_functions import generate_link
from tgbot.utils.states import Linepay

router_linepay = Router()


@router_linepay.callback_query(F.data == "linepay_deposit")
async def input_amount_inepay(call: CallbackQuery, state: FSM, user: UserDB, bot: Bot, ):
    await state.clear()
    text = f'<b>Введите сумму пополнения</b>'
    await call.message.answer(text=text, reply_markup=close_this)
    await call.answer()
    await state.set_state(Linepay.sum)


@router_linepay.message(Linepay.sum, F.text)
async def send_link_linepay(message: Message, state: FSM, user: UserDB):
    if is_number(message.text):
        amount = message.text.replace(",", ".")
        order_id = write_recipient(user_id=user.user_id, amount=amount, status="Не оплоченно")

        link, hash_md5 = generate_link(amount,order_id)
        update_recipient(id=order_id, hashmd5=hash_md5)
        text = f"Для пополнения баланса на {amount} p. нажмите на кнопку оплатить. После оплаты деньги зачислятся на Ваш баланс в боте в течении 3х минут"
        await message.answer(text=text, reply_markup=pay_linepay(link))
    else:
        await message.answer('Некорректный ввод, поторите попытку ', reply_markup=close_this)
