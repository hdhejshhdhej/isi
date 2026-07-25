from aiogram import Router

from tgbot.routers.wallet.deposit import router_deposit
from tgbot.routers.wallet.withdraw import router_withdraw


def setup_wallet_handlers(wallet_router: Router):
    wallet_router.include_router(router_deposit)
    wallet_router.include_router(router_withdraw)
















