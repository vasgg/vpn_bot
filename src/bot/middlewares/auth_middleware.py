from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.controllers.crud.user import add_user_to_db, get_user_from_db_by_tg_id


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        db_session = data['db_session']
        user = await get_user_from_db_by_tg_id(event.from_user.id, db_session)
        if not user:
            user = await add_user_to_db(event.from_user, db_session)
        data['user'] = user
        return await handler(event, data)
