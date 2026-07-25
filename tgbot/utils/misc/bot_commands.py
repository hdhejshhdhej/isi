# - *- coding: utf- 8 - *-
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from tgbot.config import ADMINS

# Команды для юзеров
user_commands = [
    BotCommand(command="start", description="♻ Перезапустить бота"),
]

# Команды для админов
admin_commands = [
    BotCommand(command="start", description="♻ Перезапустить бота"),
    BotCommand(command="admin", description="🌀 Aдмин меню"),
]


# Установка команд
async def set_commands(bot: Bot):
    await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())

    for admin in ADMINS:
        try:
            await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin))
        except:
            pass
