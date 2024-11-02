from typing import Any, Awaitable, Callable, override

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
import sentry_sdk


class AiogramSentryContextMiddleware(BaseMiddleware):
    @override
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        sentry_sdk.set_context("aiogram_event", event.model_dump(mode="json"))
        return await handler(event, data)
