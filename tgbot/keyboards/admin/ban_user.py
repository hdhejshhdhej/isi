
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.utils.const_functions import ikb



def usr_info(ban,user_id):
    if ban:
        keyboard = InlineKeyboardBuilder(
        ).row(
            ikb("Рзблокировать", data=f"blocked_user;{user_id}")
        )
    else:
        keyboard = InlineKeyboardBuilder(
        ).row(
                ikb("Заблокировать", data=f"unblocked_user;{user_id}")
            )
    return keyboard.as_markup()