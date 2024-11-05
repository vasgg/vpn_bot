import asyncio
import logging
import os

from aiogram import Bot
from asyncio import Queue, Task

from bot.config import settings

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    folder = os.path.basename(os.getcwd())
    try:
        await bot.send_message(
            settings.bot.ADMINS[0],
            f'<b>{folder.replace("_", " ")} started</b>\n\n/start',
            disable_notification=True,
        )
    except:
        logger.warning("Failed to send on shutdown notify")


async def on_shutdown(bot: Bot, queue: Queue, task: Task, event: asyncio.Event):
    await queue.join()
    event.set()
    await task
    folder = os.path.basename(os.getcwd())
    try:
        await bot.send_message(
            settings.bot.ADMINS[0],
            f'<b>{folder.replace("_", " ")} shutdown</b>',
            disable_notification=True,
        )
    except:
        logger.warning("Failed to send on shutdown notify")
