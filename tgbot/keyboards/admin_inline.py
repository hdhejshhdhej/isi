# - *- coding: utf- 8 - *-
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.utils.const_functions import ikb

my_wallet = InlineKeyboardBuilder(
).row(
    ikb("⬇️Пополнить", data='deposit'),
    ikb("⬆️ Вывести", data="withdraw"),
).row(
    ikb("↔️Перевод другому пользователю", data="withdraw_in")).as_markup()

back_wallet = InlineKeyboardBuilder().row(ikb("⬅ Назад", data="wallet")).as_markup()


def new_balance_user_in(user_id, amout):
    keyboard = InlineKeyboardBuilder(
    ).row(
        ikb("Пополнить", data=f"new_ballance_in;{user_id};{amout}"), ikb("Отмена", data="close_this")
    )
    return keyboard.as_markup()

def new_balance(user_id,amout):
    keyboard = InlineKeyboardBuilder(
    ).row(
            ikb("Пополнить", data=f"new_ballance;{user_id};{amout}"), ikb("Отмена", data="close_this")
        )

    return keyboard.as_markup()