from aiogram import Router, Bot, F
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.admin.faq_inline import create_faq, edit_faq
from tgbot.keyboards.admin.main import close_this
from tgbot.services.api_sqlite import write_faq, get_faq, get_all_faq
from tgbot.utils.misc.bot_models import FSM
from tgbot.utils.states import NewFaq

admin_faq_router = Router()


@admin_faq_router.message(Text(text="FAQ"))
async def faq_admin_main(message:Message, state:FSM, ):
    await state.clear()
    all_faq = get_all_faq()

    text = "Выберете раздел для редактирования либо создайте новый"
    await message.answer(text=text, reply_markup=create_faq(all_faq))

@admin_faq_router.callback_query(Text(text="create_faq"))
async def new_faq(call:CallbackQuery, state:FSM):
    await state.clear()
    text = "Отправьте название кнопки"
    await call.message.answer(text=text, reply_markup=close_this)
    await state.set_state(NewFaq.button)
    await call.answer()


@admin_faq_router.message(NewFaq.button, F.text)
async def button_faq(message:Message, state:FSM):
    await state.update_data(button=message.text)
    text = "Отправтьте описание"
    await message.answer(text=text)
    await state.set_state(NewFaq.description)

@admin_faq_router.message(NewFaq.button)
async def not_text_button_faq(message:Message, state:FSM):
    text = "Нужно отправить текст"
    await message.answer(text=text)

@admin_faq_router.message(NewFaq.description, F.text)
async def write_faq_handler(message:Message, state:FSM):
    description = message.html_text
    data = await state.get_data()
    text_button = data['button']
    write_faq(name_button=text_button, description=description )
    all_faq = get_all_faq()
    text = "Выберете раздел для редактирования либо создайте новый"
    await message.answer(text=text, reply_markup=create_faq(all_faq))

@admin_faq_router.message(NewFaq.description, F.text)
async def not_write_faq(message:Message,):
    text = "Нужно отправить текст"
    await message.answer(text=text)


@admin_faq_router.callback_query(F.data.startswith("edit_faq"))
async def edit_faq_handler(call:CallbackQuery, state:FSM):
    await state.clear()
    line = int(call.data.split(';')[1])
    info = get_faq(id=line)
    is_show = info['is_show']
    text_ru = f"{info['description']}\n\n"
    text = text_ru
    await call.message.edit_text(text=text, reply_markup=edit_faq(line,is_show))



