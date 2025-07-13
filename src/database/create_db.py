from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator
from src.config.config import DATABASE_URL
from src.database.models import (
    Base,
    Monitor,
    Text,
    Picture,
    User,
)
from src.func.api_func import get_all_picture_models, screen_data

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,
    poolclass=NullPool,
)

async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session


async def create_db() -> None:
    text_data = await get_all_picture_models(model_data='text')
    picture_data = await get_all_picture_models(model_data='picture')
    if text_data and picture_data:
        text = [Text(value= i) for i in text_data]
        picture = [Picture(value= i) for i in picture_data]
        monitor = [Monitor(name=key, height=value[0], weight=value[1]) for key, value in screen_data ]

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        async with async_session_maker.begin() as session:
            session.add_all(text)
            session.add_all(monitor)
            session.add_all(picture)
            await session.commit()
    else:
        print('Ошибка при формировании базы данных, во время запроса о текстовых и картинкогенерирующих моделях.')
