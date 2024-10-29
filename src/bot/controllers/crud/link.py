from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Link


async def get_links_by_user_id(user_tg_id: int, db_session: AsyncSession) -> list[Link.url]:
    query = select(Link.url).filter(Link.user_tg_id == user_tg_id)
    result: Result = await db_session.execute(query)
    links = result.scalars()
    return list(links)
