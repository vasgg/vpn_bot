import logging
from asyncio import run
from datetime import UTC, datetime, timedelta

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from sentry_sdk import init

from bot.config import Settings
from bot.controllers.crud.user import get_all_users
from bot.internal.config_dicts import setup_logs
from bot.internal.enums import Stage
from bot.internal.keyboards import buy_subscription_kb
from database.database_connector import DatabaseConnector, get_db


async def run_task(db: 'DatabaseConnector',
                   bot: 'Bot'):
    async with db.session_factory() as db_session:
        users = await get_all_users(db_session)
        now = datetime.now(UTC)
        for user in users:
            logging.debug(f"Checking user {user}...")
            if user.expired_at is None:
                continue
            tomorrow = now + timedelta(days=1)
            logging.debug(f"Left bound: {now}")
            logging.debug(f"Right bound: {tomorrow}")
            user_expiring = now < user.expired_at.replace(tzinfo=UTC) < tomorrow
            if user_expiring:
                logging.info(f"User expiring: {user}, notifying")
                await bot.send_message(
                    chat_id=user.tg_id,
                    text='Your subscription expires tomorrow\n',
                    reply_markup=buy_subscription_kb(demo_access_used=True))


async def main():
    setup_logs('cron')
    settings = Settings()
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

    db = get_db(settings)

    logging.debug("task started")
    await run_task(db, bot)
    logging.debug("task ended")


def run_main():
    run(main())


if __name__ == '__main__':
    run_main()
