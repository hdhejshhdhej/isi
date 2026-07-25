from aiogram.utils.i18n.middleware import I18nMiddleware
from aiogram import types
from typing import Tuple, Any
from tgbot.services.api_sqlite import get_userx
from pathlib import Path
from aiogram.utils.i18n.core import I18n
from  aiogram.types import TelegramObject
from typing import Dict


i18n_domain = "bot_translate"
LOCALES_DIR = 'locales/'
i18n_cl = I18n(path=LOCALES_DIR, default_locale="en", domain=i18n_domain)

async def get_lang(user_id):
    # Делаем запрос к базе, узнаем установленный язык
    user = get_userx(user_id=user_id)
    if user is not None:
        if user['lang'] is None:
            return 'en'
        return user['lang']



class LangMiddleware(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any], **kwargs) -> str:
        user = data.get('event_from_user', 0)
        # user = types.User.get_current()
        return await get_lang(user.id) or user.language_code