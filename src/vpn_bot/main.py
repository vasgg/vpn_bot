import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from database.database_connector import get_db
from vpn_bot.internal.commands import set_bot_commands
from vpn_bot.internal.lifespan import on_shutdown, on_startup
from vpn_bot.middlewares.auth_middleware import AuthMiddleware
from vpn_bot.middlewares.session_middleware import DBSessionMiddleware
from vpn_bot.middlewares.updates_dumper_middleware import UpdatesDumperMiddleware
from vpn_bot.handlers.base_handlers import router as base_router
from vpn_bot.handlers.errors_handler import router as errors_router
from vpn_bot.internal.logging_config import setup_logs

from vpn_bot.config import Settings


async def main():
    setup_logs()

    settings = Settings()

    session = AiohttpSession(timeout=120)

    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session,
    )

    logging.info("bot started")
    storage = MemoryStorage()

    dispatcher = Dispatcher(storage=storage, settings=settings)
    db = get_db(settings)

    dispatcher.update.outer_middleware(UpdatesDumperMiddleware())
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)
    dispatcher.startup.register(set_bot_commands)
    db_session_middleware = DBSessionMiddleware(db)
    dispatcher.message.middleware(db_session_middleware)
    dispatcher.callback_query.middleware(db_session_middleware)
    dispatcher.message.middleware(AuthMiddleware())
    dispatcher.callback_query.middleware(AuthMiddleware())
    dispatcher.include_routers(
        base_router,
        errors_router,
    )

    await dispatcher.start_polling(bot)


def run_main():
    asyncio.run(main())


if __name__ == '__main__':
    run_main()
