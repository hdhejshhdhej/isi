# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from tgbot.keyboards.admin.main import admin_menu, users_admin_menu
from tgbot.services.api_sqlite import get_usersx, get_all_usersx
from tgbot.utils.misc.bot_models import UserDB, FSM, RS

from tgbot.config import PATH_DATABASE, PATH_LOGS
from tgbot.utils.const_functions import get_date

router_admin_menu = Router()


# Кнопка - Admin Inline
@router_admin_menu.message(Text(text="⬅ Админ меню"))
@router_admin_menu.message(Command(commands=["admin"]))
async def admin_menu_(message: Message, bot: Bot, state: FSM, rSession: RS, user: UserDB):
    await state.clear()
    await message.answer("Админ меню", reply_markup=admin_menu())


@router_admin_menu.message(Text(text="Отмена"))
async def cancel_handler(message: Message, state: FSM) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Cancelled.", reply_markup=admin_menu(), )


# Получение Базы Данных и логов
@router_admin_menu.message(Text(text="Logs&db"))
async def admin_download_log_db(message: Message, bot: Bot, state: FSM, rSession: RS, user: UserDB):
    await state.clear()
    await message.answer_document(FSInputFile(PATH_DATABASE),
                                  caption=f"<b>📦 BACKUP</b>\n"
                                          f"<code>🕰 {get_date()}</code>")
    await message.answer_document(FSInputFile(PATH_LOGS), caption=f"<code>🕰 {get_date()}</code>")


@router_admin_menu.message(Text(text="Пользователи"))
async def admin_menu_(message: Message, bot: Bot, state: FSM, rSession: RS, user: UserDB):
    await state.clear()
    await message.answer("Выберете что нужно сделать", reply_markup=users_admin_menu)
