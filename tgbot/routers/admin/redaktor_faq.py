from aiogram import Router, Bot, F
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.admin.faq_inline import edit_faq, create_faq
from tgbot.services.api_sqlite import update_faq, get_faq, delete_faq, get_all_faq
from tgbot.utils.misc.bot_models import FSM
from tgbot.utils.states import EditFaq

admin_faq_edit = Router()


@admin_faq_edit.callback_query(F.data.startswith("description_faq"))
async def description_faq_handler(call:CallbackQuery, state:FSM):
    await state.clear()
    data = call.data.split(';')
    language_code, line = data[1], data[2]
    text = f"Отправьте новое описание"
    await call.message.answer(text=text)
    await state.set_state(EditFaq.description)
    await state.update_data(language_code=language_code, line=line)

@admin_faq_edit.message(EditFaq.description, F.text)
async def write_description_faq_handler(message:Message, state:FSM):
    description = message.html_text
    data = await state.get_data()
    language_code = data['language_code']
    line = data['line']
    if language_code == 'ru':
        update_faq(id=line, description=description)
    else:
        update_faq(id=line, description_en=description)
    info = get_faq(id=line)
    is_show = info['is_show']
    text_ru = f"{info['description']}\n\n "
    text = text_ru
    await message.answer(text=text, reply_markup=edit_faq(line, is_show))


@admin_faq_edit.callback_query(F.data.startswith("button_faq"))
async def button_faq_handler(call:CallbackQuery, state:FSM):
    await state.clear()
    data = call.data.split(';')
    language_code, line = data[1], data[2]
    text = f"Отправьте новое название кнопки"
    await call.message.answer(text=text)
    await state.set_state(EditFaq.button)
    await state.update_data(language_code=language_code, line=line)

@admin_faq_edit.message(EditFaq.button, F.text)
async def write_button_faq_handler(message:Message, state:FSM):
    name_button = message.html_text
    data = await state.get_data()
    language_code = data['language_code']
    line = data['line']
    if language_code == 'ru':
        update_faq(id=line, name_button=name_button)
    else:
        update_faq(id=line, name_button_en=name_button)
    info = get_faq(id=line)
    is_show = info['is_show']
    text_ru =  f"{info['description']}\n\n "
    text = text_ru
    await message.answer(text=text, reply_markup=edit_faq(line, is_show))



@admin_faq_edit.message(EditFaq.description)
async def not_write_description_faq_handler(message: Message, state: FSM):
    await message.answer("Нужно отправить текст")


@admin_faq_edit.callback_query(F.data.startswith("faq_is_show"))
async def show_faq_handler(call:CallbackQuery):
    data = call.data.split(';')
    is_show, line = data[1],data[2]
    update_faq(id=line, is_show=is_show)
    info = get_faq(id=line)
    await call.message.edit_reply_markup( reply_markup=edit_faq(line, info['is_show']))


@admin_faq_edit.callback_query(F.data.startswith("del_faq"))
async def del_faq_handler(call:CallbackQuery):
    data = call.data.split(';')
    line = data[1]
    delete_faq(id=line)
    all_faq = get_all_faq()
    text = "Выберете раздел для редактирования либо создайте новый"
    await call.message.edit_text(text=text, reply_markup=create_faq(all_faq))



@admin_faq_edit.callback_query(Text(text="back_faq"))
async def back_faq_handler(call:CallbackQuery):
    all_faq = get_all_faq()
    text = "Выберете раздел для редактирования либо создайте новый"
    await call.message.edit_text(text=text, reply_markup=create_faq(all_faq))


