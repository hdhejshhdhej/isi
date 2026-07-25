# - *- coding: utf- 8 - *-
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.middlewares import i18n_cl
from tgbot.utils.const_functions import ikb
from tgbot.config import ADMINS
from tgbot.services.api_sqlite import get_paymentx
from tgbot.utils.const_functions import rkb

i18n = i18n_cl
_ = lambda text: text
def payment_default():
    payment_kb = ReplyKeyboardBuilder()
    payment = get_paymentx()
    payment_kb.add(rkb("🥝 Изменить QIWI 🖍"), rkb("🥝 Проверить QIWI ♻"), rkb("🥝 Баланс QIWI 👁"))
    if payment[5] == "True":
        payment_kb.add(rkb("🔴 Выключить пополнения"))
    else:
        payment_kb.add(rkb("🟢 Включить пополнения"))
    payment_kb.add(rkb("⬅ Админ меню"),)
    return payment_kb.adjust(3,1,1).as_markup(resize_keyboard=True)

def choice_way_input_payment_func():
    get_payments = get_paymentx()
    payment_method = InlineKeyboardBuilder()

    if get_payments[4] == "form":
        payment_method.add(ikb(text="✅ По форме", data="..."))
    else:
        payment_method.add(ikb(text="❌ По форме", data="change_payment:form"))

    if get_payments[4] == "number":
        payment_method.add(ikb(text="✅ По номеру", data="..."))
    else:
        payment_method.add(ikb(text="❌ По номеру", data="change_payment:number"))

    if get_payments[4] == "nickname":
        payment_method.add(ikb(text="✅ По никнейму", data="..."))
    else:
        payment_method.add(ikb(text="❌ По никнейму", data="change_payment:nickname"))


    return payment_method.adjust(2).as_markup()


def create_pay_qiwi_func(send_requests, receipt, message_id, way):
    check_qiwi_pay_inl = InlineKeyboardBuilder()
    check_qiwi_pay_inl.add(ikb(text=_("🌀 Перейти к оплате"), url=send_requests))
    check_qiwi_pay_inl.add(ikb(text=_("🔄 Проверить оплату"), data=f"Pay:{way}:{receipt}:{message_id}"))
    return check_qiwi_pay_inl.as_markup()



