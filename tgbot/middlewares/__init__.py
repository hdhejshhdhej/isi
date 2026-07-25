# - *- coding: utf- 8 - *-
from aiogram import Dispatcher

from tgbot.middlewares.exists_user import ExistsUserMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware
from tgbot.middlewares.i18n import LangMiddleware, i18n_cl
from pathlib import Path
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware



# Подключение миддлварей
def register_all_middlwares(dp: Dispatcher):
    dp.callback_query.outer_middleware(ExistsUserMiddleware())
    dp.message.outer_middleware(ExistsUserMiddleware())

    dp.message.middleware(ThrottlingMiddleware())
    # dp.message.middleware(LangMiddleware(i18n_cl))
  
