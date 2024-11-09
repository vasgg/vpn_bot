import logging
import os

from aiogram import Bot

from bot.config import Settings

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, settings: Settings):
    folder = os.path.basename(os.getcwd())
    try:
        await bot.send_message(
            settings.bot.ADMINS[0],
            f'<b>{folder.replace("_", " ")} started</b>\n\n/start',
            disable_notification=True,
        )
    except:
        logger.warning("Failed to send on shutdown notify")


async def on_shutdown(bot: Bot, settings: Settings):
    folder = os.path.basename(os.getcwd())
    try:
        await bot.send_message(
            settings.bot.ADMINS[0],
            f'<b>{folder.replace("_", " ")} shutdown</b>',
            disable_notification=True,
        )
    except:
        logger.warning("Failed to send on shutdown notify")
