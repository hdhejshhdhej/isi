# - *- coding: utf- 8 - *-
from aiogram import Dispatcher, Router, F

from tgbot.config import ADMINS
from tgbot.routers.admin import setup_admin_handlers
from tgbot.routers.feed_back_group import router_feed_back
from tgbot.routers.main_start import router_start
from tgbot.routers.user import setup_user_handlers
from tgbot.routers.errors import router_errors
from tgbot.routers.wallet import setup_wallet_handlers
from tgbot.routers.z_all_missed import router_missed



# Подключение всех роутеров
def register_all_routers(dp: Dispatcher):
    # Создание образов роутера
    user_router = Router()
    admin_router = Router()

    # Инициализация системных роутеров
    dp.include_router(router_start)
    dp.include_router(router_errors)
    # Подгрузка хендлеров в роутеры
    setup_admin_handlers(admin_router)
    setup_user_handlers(user_router)
    setup_wallet_handlers(user_router)
    dp.include_router(router_feed_back)
    # Подключение фильтров
    admin_router.callback_query.filter(F.from_user.id.in_(ADMINS) ) # & admin_router.callback_query.filter(F.chat.type == "private")

    admin_router.message.filter(F.from_user.id.in_(ADMINS))# & F.chat.type == "private")
    # admin_router.message.filter(F.chat.type == "private")
    # user_router.callback_query.filter(F.chat.type == "private")
    user_router.message.filter(F.chat.type == "private")

    # Инициализация рабочих роутеров
    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.include_router(router_missed)




