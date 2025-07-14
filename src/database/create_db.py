import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from src.config.config import DATABASE_URL
from src.database.models import (
    Base,
    Monitor,
    Picture,
    Text,
)
from src.func.api_func import get_all_picture_models

screen_data: dict = {
    "samsung_a40_1080x2340": [1080, 2340],
    "1280_1024": [1280, 1024],
    "1366_768": [1366, 768],
    "1440_900": [1440, 900],
    "1600_900": [1600, 900],
    "1680_1050": [1680, 1050],
    "1920_1080": [1920, 1200],
    "1920_1200": [1920, 1200],
    "2560_1080": [2560, 1080],
    "2560_1440": [2560, 1440],
    "3440_1440": [3440, 1440],
    "3840_2160": [3840, 2160],
    "4096_2160": [4096, 2160],
    "5120_2880": [5120, 2880],
}

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
    """
    Функция создания базы данных
    :return:
    """
    text_data: list | None = await get_all_picture_models(model_data="text")
    picture_data: list | None = await get_all_picture_models(model_data="picture")
    if text_data and picture_data:
        text: list = [Text(value=i) for i in text_data]
        picture: list = [Picture(value=i) for i in picture_data]
        monitor: list = [
            Monitor(name=key, width=value[0], height=value[1])
            for key, value in screen_data.items()
        ]

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        async with async_session_maker.begin() as session:
            session.add_all(text)
            session.add_all(monitor)
            session.add_all(picture)
    else:
        logging.warning(msg="Ошибка при формировании базы данных, во"
            " время запроса о текстовых и картинкогенерирующих моделях.")
