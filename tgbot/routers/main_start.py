# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import Command, Text
from aiogram.types import Message

from tgbot.keyboards.z_all_reply import user_menu
from tgbot.utils.misc.bot_models import UserDB, FSM, RS

router_start = Router()
router_start.message.filter(F.chat.type == 'private')

# Открытие главного меню
@router_start.message(Command(commands="start"))
@router_start.message(Text(text="⬅ Главное меню"))
async def main_starte(message: Message, state: FSM, ):
    await state.clear()
    await message.answer("🔸 Бот готов к использованию.\n"
                         "🔸 Если не появились вспомогательные кнопки\n"
                         "▶ Введите /start",
                         reply_markup=user_menu())
