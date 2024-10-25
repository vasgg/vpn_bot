import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from database.database_connector import get_db
from database.models import Base
from bot.config import settings


async def create_or_drop_db(engine: AsyncEngine, create: bool = True):
    async with engine.begin() as conn:
        if create:
            await conn.run_sync(Base.metadata.create_all, checkfirst=True)
        else:
            await conn.run_sync(Base.metadata.drop_all)


async def populate_db(db_session: AsyncSession):
    ...

    await db_session.commit()


async def main():
    db = get_db(settings)
    await create_or_drop_db(db.engine, False)
    await create_or_drop_db(db.engine)
    async with db.session_factory.begin() as session:
        await populate_db(session)


def run_main():
    asyncio.run(main())


if __name__ == '__main__':
    run_main()
