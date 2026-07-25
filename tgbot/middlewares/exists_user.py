# - *- coding: utf- 8 - *-
from aiogram import BaseMiddleware, types

from tgbot.services.api_sqlite import get_userx, add_userx, delete_userx, update_userx
from tgbot.utils.const_functions import clear_html
from tgbot.utils.misc.bot_models import WrapperMapDict, UserDB


# Проверка юзеров в БД и их добавление
class ExistsUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: types.Message, data):
        get_user = event.from_user
        # если это пользователь
        if not get_user.is_bot:
            user_id = get_user.id
            user_name = get_user.username
            first_name = clear_html(get_user.first_name)
            last_name = clear_html(get_user.last_name)

            get_user_id = get_userx(user_id=user_id)
            # если новый пользователь
            if get_user_id is None:
                if user_name is not None:
                    add_userx(user_id, user_name.lower(), first_name, last_name)
                else:
                    add_userx(user_id, user_name, first_name, last_name)
                # рефералка добавидь в БД поле referral_id  int
                # if event.content_type == 'text' and event.text[:6] == '/start':
                #     if len(event.text.split()) == 2:
                #         referral = get_userx(user_id=int(event.text.split()[1]))
                #         if referral is not None:
                #             referral_id = referral['user_id']
                #             update_userx(user_id, referral_id=referral_id)
            else:
                # Бан добавить столбец ban int or bool
                if get_user_id['ban']:
                    return
                if first_name != get_user_id['first_name']:
                    update_userx(get_user_id['user_id'], first_name=first_name)
                if last_name != get_user_id['last_name']:
                    update_userx(get_user_id['user_id'], last_name=last_name)
                if user_name is not None:
                    if user_name.lower() != get_user_id['user_name']:
                        update_userx(get_user_id['user_id'], user_name=user_name.lower())
                else:
                    update_userx(get_user_id['user_id'], user_name=None)


            data['user'] = UserDB(**get_userx(user_id=user_id))

        return await handler(event, data)
