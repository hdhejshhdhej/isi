# - *- coding: utf- 8 - *-
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tgbot.utils.const_functions import rkb





# Тестовые юзер реплай кнопки
def user_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(rkb("🔍 Поиск"),  rkb("🧍История запросов"),)
    builder.add(rkb("🏦 Кошелек"),  rkb("📊 Тарифы"),)
    builder.add(  rkb("ℹ️ Инфо"))

    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)
