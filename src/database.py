from typing import AsyncGenerator

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from configs.settings import settings



engine = create_async_engine(settings.db_dsl, echo=True)

async_sessiom_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessiom_maker() as session:
        try:
            yield session
        finally:
            await session.close()