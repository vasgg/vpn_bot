import logging

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Link

logger = logging.getLogger(__name__)


async def get_links_by_user_id(user_tg_id: int, db_session: AsyncSession) -> list[Link]:
    query = select(Link).filter(Link.user_tg_id == user_tg_id)
    result: Result = await db_session.execute(query)
    links = list(result.scalars())
    logger.info(f"Loaded links for user {user_tg_id}: {links=}, length: {len(links)}")
    return links


async def update_links_url(user_tg_id: int, new_urls: list[str], db_session: AsyncSession):
    links = await get_links_by_user_id(user_tg_id, db_session)
    if len(new_urls) != len(links):
        raise ValueError("Length of new_urls must be equal to length of links")
    for link, new_url in zip(links, new_urls):
        link.url = new_url
        logger.info(f"Updated link for user {user_tg_id}: {link}")
