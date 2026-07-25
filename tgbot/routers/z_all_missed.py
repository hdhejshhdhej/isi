# - *- coding: utf- 8 - *-
from aiogram import types, Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tgbot.utils.misc.bot_models import FSM

router_missed = Router()


@router_missed.callback_query(F.data == "close_this")
async def processing_callback_remove(call: CallbackQuery, state: FSM):
    await state.clear()
    await call.message.delete()


# Колбэк с обработкой кнопки
@router_missed.callback_query(F.data == "...")
async def processing_callback_answer(call: CallbackQuery, state: FSM):
    await call.answer(cache_time=20)


# Колбэк с обработкой удаления сообщений потерявших стейт
@router_missed.callback_query()
async def processing_callback_missed(call: CallbackQuery, state: FSM):
    try:
        await call.message.delete()
    except:
        pass
    await call.message.answer("<b>❌ Данные не были найдены из-за перезапуска скрипта.\n"
                              "♻ Выполните действие заново.</b>",
                              )


# Обработка всех неизвестных команд
@router_missed.message()
async def processing_message_missed(message: types.Message, bot: Bot):
    await message.answer("♦ Неизвестная команда.\n"
                         "▶ Введите /start")
