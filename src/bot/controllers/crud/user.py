from datetime import UTC, datetime
import logging

from dateutil.relativedelta import relativedelta
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.controllers.helpers import compose_username
from database.models import User

logger = logging.getLogger(__name__)


async def add_user_to_db(user, db_session: AsyncSession) -> User:
    new_user = User(tg_id=user.id, fullname=user.full_name, username=compose_username(user))
    db_session.add(new_user)
    await db_session.flush()
    logger.info(f"New user created: {new_user}")
    return new_user


async def get_user_from_db_by_tg_id(telegram_id: int, db_session: AsyncSession) -> User | None:
    query = select(User).filter(User.tg_id == telegram_id)
    result: Result = await db_session.execute(query)
    user = result.scalar_one_or_none()
    return user


async def update_db_user_expiration(user: User, duration: relativedelta, db_session: AsyncSession):
    current_time = datetime.now(UTC)
    if user.expired_at > current_time:
        user.expired_at += duration
    else:
        user.expired_at = current_time + duration
    db_session.add(user)
    logger.info(f"Subscription for {user.tg_id} prolonged to {user.expired_at}")
    return user.expired_at
