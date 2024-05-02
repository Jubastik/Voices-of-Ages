import asyncio
import logging
import platform

import coloredlogs
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis

from src.dialogs import register_dialogs
from src.commands import setup_bot_commands, remove_bot_commands
from src.dialogs.main_router import dlg_router, error_handler
from src.settings import settings
from urllib.parse import urlparse


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    bot_info = await bot.get_me()

    logging.info(f"Name - {bot_info.full_name}")
    logging.info(f"Username - @{bot_info.username}")
    logging.info(f"ID - {bot_info.id}")

    states = {
        True: "Enabled",
        False: "Disabled",
    }
    logging.debug(f"Groups Mode - {states[bot_info.can_join_groups]}")
    logging.debug(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logging.debug(f"Inline Mode - {states[bot_info.supports_inline_queries]}")
    logging.error("Bot started!")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.warning("Stopping bot...")
    await remove_bot_commands(bot)
    await dispatcher.fsm.storage.close()
    await bot.session.close()


async def main():
    coloredlogs.install(level=logging.INFO)
    logging.warning("Starting bot...")

    # Initializing REDIS for FSM
    storage = RedisStorage(
        redis=Redis(host=settings.redis_url.host,
                    port=settings.redis_url.port,
                    db=settings.redis_url.path.lstrip('/') or 0,
                    password=settings.redis_url.password),
        key_builder=DefaultKeyBuilder(with_destiny=True)
    )

    # Initializing the dispatcher
    bot = Bot(token=settings.token.get_secret_value(), default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=storage)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.errors.register(error_handler)
    register_dialogs(dp)

    # Registration of routes
    dp.include_router(dlg_router)
    setup_dialogs(dp)
    await setup_bot_commands(bot)
    await dp.start_polling(bot, on_shutdown=on_shutdown, on_startup=on_startup)


if __name__ == "__main__":
    try:
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
