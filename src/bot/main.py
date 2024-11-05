from asyncio import run
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from sentry_sdk import init

from bot.internal.enums import Stage
from bot.middlewares.auth_middleware import AuthMiddleware
from database.database_connector import get_db
from bot.internal.commands import set_bot_commands
from bot.internal.notify_admin import on_shutdown, on_startup
from bot.middlewares.session_middleware import DBSessionMiddleware
from bot.middlewares.updates_dumper_middleware import UpdatesDumperMiddleware
from bot.handlers.base_handlers import router as base_router
from bot.handlers.errors_handler import router as errors_router
from bot.handlers.payment_handlers import router as payment_router
from bot.internal.config_dicts import setup_logs

from bot.config import settings


async def main():
    setup_logs('vpn_bot')

    if settings.bot.SENTRY_DSN and settings.bot.STAGE == Stage.PROD:
        init(
            dsn=settings.bot.SENTRY_DSN.get_secret_value(),
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )

    session = AiohttpSession(timeout=120)

    bot = Bot(
        token=settings.bot.TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session,
    )

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
        payment_router,
    )

    await dispatcher.start_polling(bot)
    logging.info("VPN bot started")


def run_main():
    run(main())


if __name__ == '__main__':
    run_main()
