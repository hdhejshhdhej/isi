# - *- coding: utf- 8 - *-
import asyncio

from aiogram import Router, Bot, F
from aiogram.filters import Text
from aiogram.types import FSInputFile, Message
from aiogram.exceptions import TelegramForbiddenError

from tgbot.keyboards.admin.main import admin_menu
from tgbot.utils.const_functions import get_date

from tgbot.utils.states import Sender
from tgbot.utils.misc.bot_models import UserDB, FSM, RS

from tgbot.keyboards.z_all_inline import sender_button
from tgbot.keyboards.admin.main import skip, send_all

from tgbot.services.api_sqlite import get_all_usersx

router_sender = Router()

# Кнопка Рассылка
@router_sender.message(Text(text="✉️ Рассылка"))
async def great_post(message: Message,  state: FSM):
    await state.set_state(Sender.text)
    text = '<b>Длина одного сообщения без фото до 4 096 символов Длина одного сообщения c фото до 1 024 символов\n' \
           'Отправьте отформатированый текст</b>'
    await message.answer(text, reply_markup=skip)

# сообщение без текста
@router_sender.message(Sender.text, F.text.casefold() == "пропустить")
async def process_skip_text_send_photo(message: Message, state: FSM) -> None:
    await state.update_data(text=None)
    await state.set_state(Sender.photo)
    await message.answer('<b>Отправьте фото 📷 или пропустите этот шаг</b>', reply_markup=skip)

# текст сообщения
@router_sender.message(Sender.text, F.text)
async def process_text_post_send_photo(message: Message, state: FSM) -> None:
    await state.update_data(text=message.html_text)
    await state.set_state(Sender.photo)
    await message.answer('<b>Отправьте фото 📷 или пропустите этот шаг</b>', reply_markup=skip)

# обработчик ошибки если отправлен не текст
@router_sender.message(Sender.text)
async def process_text_post_err(message: Message, state: FSM) -> None:
    await message.answer('⛔<b>️Нужно отправить текст</b>', reply_markup=skip)

# сообщение без фото
@router_sender.message(Sender.photo, F.text.casefold() == "пропустить")
async def process_spip_photo_post(message: Message, state: FSM) -> None:
    data = await state.update_data(photo=None)
    if data['text'] is None:
        await message.answer('<b>️Сообщение не может быть без текста и изображения. Действие отменнено</b>',
                             reply_markup=admin_menu())
        await state.clear()
        return
    await state.set_state(Sender.button)
    await message.answer('<b>Укажите название кнопки  </b>', reply_markup=skip)

# фото
@router_sender.message(Sender.photo, F.photo)
async def process_photo_post_name_button(message: Message, state: FSM) -> None:
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await state.set_state(Sender.button)
    await message.answer('<b>Укажите название кнопки  </b>', reply_markup=skip)

# обработчик ошибки если отправлен не фото
@router_sender.message(Sender.photo)
async def process_photo_post_err(message: Message) -> None:
    await message.answer('<b>️Не коректный ввод, повторите попытку </b>')

# сообщение без кнопки
@router_sender.message(Sender.button, F.text.casefold() == "пропустить")
async def process_button_send_post(message: Message, bot: Bot, state: FSM) -> None:
    await state.update_data(button=None)
    data = await state.update_data(url=None)
    text = data['text']
    photo = data['photo']
    if photo is not None:
        await bot.send_photo(message.from_user.id, photo, caption=text)
    else:
        await bot.send_message(message.from_user.id, text)
    await message.answer('<b>Проверьте пост ⬆️, если все верно нажмите кнопку отправить ⬇️</b>', reply_markup=send_all)

# отправка сообщения всем пользователям
@router_sender.message(Sender.url, F.text.casefold() == "отправить всем")
@router_sender.message(Sender.button, F.text.casefold() == "отправить всем")
async def process_sender(message: Message, bot: Bot, state: FSM) -> None:
    data = await state.get_data()
    usrs = get_all_usersx()
    text = data['text']
    photo = data['photo']
    button = data['button']
    url = data['url']
    reply = None
    if button is not None and url is not None:
        reply = sender_button(button, url)
    all_usr = 0
    send = 0
    no_send = 0
    await message.answer(f"<b>📨  START SENDER </b>\n" f"<code>🕰 {get_date()}</code>", reply_markup=admin_menu())
    for i in usrs:
        user_id = i['user_id']
        all_usr += 1
        await asyncio.sleep(.05)
        try:
            if photo is not None:
                await bot.send_photo(user_id, photo, caption=text, reply_markup=reply)
            else:
                await bot.send_message(user_id, text, reply_markup=reply)
            send += 1
        except:
            no_send += 1
            continue
    await message.answer(f"<b>📩 FINISH SENDER </b>\n"
                         f"<b>👤 All users {all_usr} </b>\n"
                         f"<b>✅ Send {send} </b>\n"
                         f"<b>❌ Not sent {no_send} </b>\n"
                         f"" f"<code>🕰 {get_date()}</code>")

# название кнопки
@router_sender.message(Sender.button, F.text)
async def process_button_post(message: Message, state: FSM) -> None:
    await state.update_data(button=message.text)
    await state.set_state(Sender.url)
    await message.answer('<b>Укажите URL </b>', reply_markup=skip)

# обработчик ошибки если отправлен не текст для кнопки
@router_sender.message(Sender.button)
async def process_button_post_err(message: Message) -> None:
    await message.answer('⛔<b>️Нужно отправить текст</b>', reply_markup=skip)

# ссылка
@router_sender.message(Sender.url, F.text.regexp(r'^(?:https|ftp)s?://'))
async def process_url_post(message: Message, bot: Bot, state: FSM) -> None:
    await message.answer(message.text, reply_markup=skip)
    data = await state.update_data(url=message.text)
    text = data['text']
    photo = data['photo']
    button = data['button']
    url = data['url']
    reply = None
    if button is not None and url is not None:
        reply = sender_button(button, url)
    if photo is not None:
        await bot.send_photo(message.from_user.id, photo, caption=text, reply_markup=reply)
    else:
        await bot.send_message(message.from_user.id, text, reply_markup=reply)
    await message.answer('<b>Проверьте пост ⬆️, если все верно нажмите кнопку отправить ⬇️</b>', reply_markup=send_all)

# обработчик ошибки если отправлен не текст ссылки
@router_sender.message(Sender.url)
async def process_url_post_err(message: Message, bot: Bot, state: FSM) -> None:
    await message.answer('<b>Нужно отправить ссылку</b>', reply_markup=skip)
