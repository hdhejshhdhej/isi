
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message, Chat

from tgbot.config import ADMIN_ANSWER_GROUP
from tgbot.keyboards.z_all_inline import feed_kb

from tgbot.services.api_sqlite import update_userx

router_feed_back = Router()
router_feed_back.message.filter(F.chat.id == ADMIN_ANSWER_GROUP)

def extract_id(message: Message) -> int:
    # Получение списка сущностей (entities) из текста или подписи к медиафайлу в отвечаемом сообщении
    entities = message.entities or message.caption_entities
    # Если всё сделано верно, то последняя (или единственная) сущность должна быть хэштегом...
    if not entities or entities[-1].type != "hashtag":
        raise ValueError("Не удалось извлечь ID для ответа!")

    # ... более того, хэштег должен иметь вид #id123456, где 123456 — ID получателя
    hashtag = message.text.split()[-1]
    if len(hashtag) < 4 or not hashtag[3:].isdigit():  # либо просто #id, либо #idНЕЦИФРЫ
        raise ValueError("Некорректный ID для ответа!")

    return int(hashtag[3:])


@router_feed_back.message(Command(commands=["get", "who"]), F.reply_to_message)
async def get_user_info(message: Message, bot: Bot):
    def get_full_name(chat: Chat):
        if not chat.first_name:
            return ""
        if not chat.last_name:
            return chat.first_name
        return f"{chat.first_name} {chat.last_name}"

    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))

    try:
        user = await bot.get_chat(user_id)
    except TelegramAPIError as ex:
        return await message.reply(f"Не удалось получить информацию о пользователе! Ошибка: {ex}")

    u = f"@{user.username}" if user.username else 'нет'
    await message.reply(f"Имя: {get_full_name(user)}\n\nID: {user.id}\nUsername: {u}")


@router_feed_back.message(Command(commands=["ban"]), F.reply_to_message)
async def cmd_ban(message: Message):
    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))
    update_userx(user_id=int(user_id), status='banned')
    await message.reply(
        f"ID {user_id} добавлен в список заблокированных. "
        f"При попытке отправить сообщение пользователь получит уведомление о том, что заблокирован."
    )

@router_feed_back.message(Command(commands=["shadowban"]), F.reply_to_message)
async def cmd_shadowban(message: Message):
    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))
    update_userx(user_id=int(user_id), status='shadowban')
    await message.reply(
        f"ID {user_id} добавлен в список  скрытно заблокированных. "
        f"При попытке отправить сообщение пользователь не узнает, что заблокирован."   )




@router_feed_back.message(Command(commands=["unban"]), F.reply_to_message)
async def cmd_unban(message: Message):
    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))
    user_id = int(user_id)
    update_userx(user_id=int(user_id), status='unbanned')
    await message.reply(f"ID {user_id} разблокирован")


@router_feed_back.message(F.reply_to_message)
async def reply_to_user(message: Message, bot:Bot):
    """
    Ответ администратора на сообщение юзера (отправленное ботом).
    Используется метод copy_message, поэтому ответить можно чем угодно, хоть опросом.
    :param message: сообщение от админа, являющееся ответом на другое сообщение
    """

    # Вырезаем ID
    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))

    # Пробуем отправить копию сообщения.
    # В теории, это можно оформить через errors_handler, но мне так нагляднее
    try:
        text = f"💬 Служба поддержки \n\n {message.text}"
        await bot.send_message(user_id, text,reply_markup=feed_kb())
    except TelegramAPIError as ex:
        await message.reply(f"Не удалось отправить сообщение адресату!\nОтвет от Telegram: {ex.message}")

