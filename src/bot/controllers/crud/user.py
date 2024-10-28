from datetime import datetime
import logging

from dateutil.relativedelta import relativedelta
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User

logger = logging.getLogger(__name__)


async def add_user_to_db(user, db_session: AsyncSession) -> User:
    new_user = User(tg_id=user.id, fullname=user.full_name, username=user.username, phone_number=user.phone_number)
    db_session.add(new_user)
    await db_session.flush()
    return new_user


async def get_user_from_db_by_tg_id(telegram_id: int, db_session: AsyncSession) -> User | None:
    query = select(User).filter(User.tg_id == telegram_id)
    result: Result = await db_session.execute(query)
    user = result.scalar_one_or_none()
    return user


async def get_all_users_ids(db_session: AsyncSession) -> list[User.tg_id]:
    query = select(User.tg_id)
    result = await db_session.execute(query)
    return list(result.scalars().all())


async def update_user_expiration(user: User, months: int, db_session: AsyncSession):
    current_time = datetime.now()
    if user.expired_at > current_time:
        user.expired_at += relativedelta(months=months)
    else:
        user.expired_at = current_time + relativedelta(months=months)
    db_session.add(user)
    logger.info(f"Подписка пользователя {user.tg_id} обновлена до {user.expired_at}")
