# - *- coding: utf- 8 - *-
import json
import random
import time

import aiohttp
from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message

from tgbot.config import PHONE
from tgbot.keyboards.admin.main import close_this
from tgbot.keyboards.qiwi_kb import payment_default, create_pay_qiwi_func
from tgbot.keyboards.z_all_inline import update_qiwi_balancce

from tgbot.middlewares import i18n_cl
from tgbot.services.api_sqlite import get_paymentx, get_userx, update_userx, add_refillx, get_refillx, new_ballance_user
from tgbot.utils.const_functions import get_date
from tgbot.utils.token_to_dollar import get_rub_in_dollars
from tgbot.utils.misc.bot_models import UserDB, FSM, RS
from tgbot.utils.misc_functions import send_admins
from tgbot.utils.states import StorageQiwi
from pyqiwip2p import QiwiP2P
from aiogram.filters import Text

router_qiwi = Router()


@router_qiwi.callback_query(Text(text="qiwi_deposit"))
async def input_amount(call: CallbackQuery, state: FSM, user: UserDB, bot: Bot,):
    await state.clear()
    text = f'<b>Адрес кошелька QIWI: <code>{PHONE}</code>\nКоментарий:   <code>{user.user_id}</code></b>'
    LINK = f'https://qiwi.com/payment/form/99?currency=643&amountFraction=0&extra[%27account%27]={PHONE}&extra[%27comment%27]={user.user_id}&blocked[2]=comment&blocked[1]=account'
    # await call.message.edit_text(text=text, reply_markup=update_qiwi_balancce(LINK))
    await call.message.edit_text(text=text, reply_markup=update_qiwi_balancce(link=LINK))
    await call.answer()