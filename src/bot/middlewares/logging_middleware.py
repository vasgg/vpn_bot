import functools
import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:

        try:
            name = self._get_name(handler)
            logging.info(f"calling {name}")
        finally:
            res = await handler(event, data)
        return res

    def _get_name(self, handler):
        while isinstance(handler, functools.partial):
            handler = handler.args[0]

        name = handler.__wrapped__.__self__.callback.__name__
        return name
