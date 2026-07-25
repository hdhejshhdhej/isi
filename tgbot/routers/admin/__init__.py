# - *- coding: utf- 8 - *-
from aiogram import Router

from tgbot.routers.admin.admin_menu import router_admin_menu
from tgbot.routers.admin.ban_user import router_ban
from tgbot.routers.admin.faq_main import admin_faq_router
from tgbot.routers.admin.new_ballance import router_new_ballance

# Подключение хендлеров для админа
from tgbot.routers.admin.qiwi_admin import router_admin_qiwi
from tgbot.routers.admin.redaktor_faq import admin_faq_edit
from tgbot.routers.admin.sender import router_sender


def setup_admin_handlers(admin_router: Router):
    admin_router.include_router(router_admin_menu)
    admin_router.include_router(router_new_ballance)
    admin_router.include_router(router_sender)
    admin_router.include_router(router_ban)
    admin_router.include_router(router_admin_qiwi)
    admin_router.include_router(admin_faq_router)
    admin_router.include_router(admin_faq_edit)



