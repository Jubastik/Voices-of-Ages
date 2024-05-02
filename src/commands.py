from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from src.settings import settings

users_commands = {
    "update": "Меню",
}

owner_commands = {**users_commands, "ping": "Пинг понг"}


async def setup_bot_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in owner_commands.items()
        ],
        scope=BotCommandScopeChat(chat_id=settings.admin_id),
    )

    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in users_commands.items()
        ],
        scope=BotCommandScopeDefault(),
    )


async def remove_bot_commands(bot: Bot):
    await bot.delete_my_commands(scope=BotCommandScopeDefault())
    await bot.delete_my_commands(
        scope=BotCommandScopeChat(chat_id=settings.admin_id)
    )
