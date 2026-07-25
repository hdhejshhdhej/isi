from aiogram.types import Message, CallbackQuery, ChatMemberUpdated

from tgbot.config import ADMIN_ANSWER_GROUP
from tgbot.utils.misc.bot_models import UserDB, FSM, RS
from aiogram import Router, Bot, F
from tgbot.utils.states import ListenMessageForward

feed_user = Router()



@feed_user.callback_query(F.data == "feed_back")
async def msg_admin_feed(call:CallbackQuery, state:FSM):
    await state.clear()
    await call.message.answer('Отправьте сообщение, Вам ответит админ.')
    await state.set_state(ListenMessageForward.message)

@feed_user.message(ListenMessageForward.message, F.text)
async def text_message(message: Message, bot: Bot, user: UserDB):
    status = str(user.feed_back)
    if len(message.text) > 4000:
        return await message.reply("К сожалению, длина этого сообщения превышает допустимый размер. "
                                   "Пожалуйста, сократи свою мысль и попробуй ещё раз.")

    if status == "banned":
        await message.answer("К сожалению, Admin бота решил тебя заблокировать, сообщения не будут доставлены.")
        return
    elif status == "shadowban":
        await message.reply('Отправлено')
        return

    else:
        await bot.send_message(
            ADMIN_ANSWER_GROUP,
            message.html_text + f"\n\n@{str(message.from_user.username)}\n"+ f"\n\n#id{message.from_user.id}", )
        await message.reply('Отправлено')


@feed_user.message(ListenMessageForward.message)
async def not_text_message(message: Message, bot: Bot, user: UserDB):
    await message.reply("К сожалению, этот тип сообщения не поддерживается. Отправь что-нибудь другое.")
