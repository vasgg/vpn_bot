import logging
import traceback

import aiogram
from aiogram import Router
from aiogram.types import ErrorEvent

from bot.config import Settings

router = Router()


@router.errors()
async def error_handler(error_event: ErrorEvent, bot: aiogram.Bot, settings: Settings):
    exc_info = error_event.exception
    exc_traceback = ''.join(
        traceback.format_exception(None, exc_info, exc_info.__traceback__),
    )
    tb = exc_traceback[-3500:]

    error_message = (
        f"🚨 <b>An error occurred</b> 🚨\n\n"
        f"<b>Type:</b> {type(exc_info).__name__}\n<b>Message:</b> {exc_info}\n\n<b>Traceback:</b>\n<code>{tb}</code>"
    )
    logging.exception("Exception: ", exc_info=exc_info)

    await bot.send_message(settings.ADMIN_ID, error_message)
