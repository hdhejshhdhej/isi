# - *- coding: utf- 8 - *-
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from tgbot.config import ADMINS
from tgbot.utils.const_functions import rkb, ikb


def admin_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(rkb("✉️ Рассылка"))
    builder.add(rkb("Logs&db"))
    builder.add(rkb("Qiwi"))
    builder.add(rkb("FAQ"))
    builder.add(rkb("⬅ Главное меню"))
    builder.adjust(2, 2, 1)
    return builder.as_markup(resize_keyboard=True)


skip = ReplyKeyboardBuilder().row(
    rkb('Пропустить'),
    rkb('Отмена')
).as_markup(resize_keyboard=True)

send_all = ReplyKeyboardBuilder().row(
    rkb('Отправить всем'),
    rkb('Отмена')
).as_markup(resize_keyboard=True)

back_admin_menu = ReplyKeyboardBuilder().row(
    rkb("⬅ Админ меню"),
    rkb("⬅ Главное меню")).as_markup(resize_keyboard=True)

users_admin_menu = ReplyKeyboardBuilder().row(
    rkb('Пополнить баланс'),
    rkb('Инфо/Бан'),
).row(
    rkb("⬅ Админ меню"),
    rkb("⬅ Главное меню")).as_markup(resize_keyboard=True)

close_this = InlineKeyboardBuilder(
).row(
    ikb("Отмена", data=f"close_this")
).as_markup()
