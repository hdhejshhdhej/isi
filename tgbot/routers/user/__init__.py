# - *- coding: utf- 8 - *-
from aiogram import Router, F

from tgbot.routers.user.avto import router_avto
from tgbot.routers.user.email import router_email
from tgbot.routers.user.faq_user import faq_user_router
from tgbot.routers.user.feed_back import feed_user
from tgbot.routers.user.inn import router_inn
from tgbot.routers.user.inn_fl import router_inn_fl
from tgbot.routers.user.name_full import router_name_full
from tgbot.routers.user.name_standart import router_people_data
from tgbot.routers.user.passport import router_passport
from tgbot.routers.user.phone import router_phone
from tgbot.routers.user.qiwi import router_qiwi
from tgbot.routers.user.scoring import router_scoring
from tgbot.routers.user.snils import router_snils
from tgbot.routers.user.user_menu import router_user_menu
from tgbot.routers.user.history import router_history
from tgbot.routers.user.vin import router_vin
from tgbot.routers.user.linepay import router_linepay
from tgbot.routers.user.kredit import router_credit

def setup_user_handlers(user_router: Router):
    user_router.include_router(router_user_menu)
    user_router.include_router(router_people_data)
    user_router.include_router(router_name_full)
    user_router.include_router(router_phone)
    user_router.include_router(router_passport)
    user_router.include_router(router_inn_fl)
    user_router.include_router(router_email)
    user_router.include_router(router_snils)
    user_router.include_router(router_avto)
    user_router.include_router(router_vin)
    user_router.include_router(router_inn)
    user_router.include_router(router_scoring)
    user_router.include_router(router_credit)
    user_router.include_router(faq_user_router)
    user_router.include_router(feed_user)
    user_router.include_router(router_history)
    user_router.include_router(router_linepay)



