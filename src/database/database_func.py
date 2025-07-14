import logging

from sqlalchemy import insert, select, update
from sqlalchemy.orm import joinedload

from src.database.create_db import get_db_session
from src.database.models import Monitor, Picture, Text, User


async def check_text_data(tel_id: int) -> str | None:
    """
    Метод для проверки данных о text models data пользователя
    :param tel_id:
    :return:
    """

    async with get_db_session() as session:
        result_data = await session.execute(
            select(User)
            .join(User.text_rel)
            .options(
                joinedload(User.text_rel),
            )
            .where(User.tel_id == tel_id)
        )
        result = result_data.scalar_one_or_none()
    return result.text_rel.value if result else None


async def check_monitor_data(tel_id: int) -> str | None:
    """
    Метод для проверки данных о monitor models data пользователя
    :param tel_id:
    :return:
    """

    async with get_db_session() as session:
        result_data = await session.execute(
            select(User)
            .join(User.monitor_rel)
            .options(joinedload(User.monitor_rel))
            .where(User.tel_id == tel_id)
        )
        result = result_data.scalar_one_or_none()
    return result.monitor_rel.name if result else None


async def check_picture_data(tel_id: int) -> str | None:
    """
    Метод для проверки данных о monitor models data пользователя
    :param tel_id:
    :return:
    """

    async with get_db_session() as session:
        result_data = await session.execute(
            select(User)
            .join(User.picture_rel)
            .options(joinedload(User.picture_rel))
            .where(User.tel_id == tel_id)
        )
        result = result_data.scalar_one_or_none()
    return result.picture_rel.value if result else None


async def get_resolution_w_h(res: str) -> tuple:
    """
    Метод возвращает разрешение по коду
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            select(Monitor).where(Monitor.name == res)
        )
        result = result_data.scalar_one_or_none()
    return result.width, result.height


async def get_resolution_data(res: str) -> Monitor | None:
    """
    Метод возвращает данных о выбранном разрешении по коду
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            select(Monitor).where(Monitor.name == res)
        )
        result = result_data.scalar_one_or_none()
    return result


async def get_picture_models(model: str) -> Picture | None:
    """
    Метод для
    :param model:
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            select(Picture).where(Picture.value == model)
        )
        result = result_data.scalar_one_or_none()
    return result


async def update_user_data_picture(tel_id: int, res: str, model: str):
    """
    Метод для
    :param model:
    :param tel_id:
    :param res:
    :return:
    """
    resolution = await get_resolution_data(res=res)
    picture = await get_picture_models(model=model)
    if resolution and picture:
        async with get_db_session() as session:
            await session.execute(
                update(User)
                .where(User.tel_id == tel_id)
                .values(monitor=resolution.id, picture=picture.id)
            )
            await session.commit()
    else:
        logging.warning('Error with db in "update_user_data_picture"')


async def get_text_model(text_model: str) -> Text | None:
    """
    Метод для возврата сущности текстовой модели
    :param text_model:
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            select(Text).where(Text.value == text_model)
        )
        result = result_data.scalar_one_or_none()
    return result


async def update_user_data_text(tel_id: int, text_model: str) -> None:
    """
    Метод для бновления последних данных для пользователя
    :param tel_id:
    :param text_model:
    :return:
    """
    text = await get_text_model(text_model=text_model)
    if text:
        async with get_db_session() as session:
            await session.execute(
                update(User)
                .where(User.tel_id == tel_id)
                .values(
                    text=text.id,
                )
            )
            await session.commit()


async def get_all_text_model() -> list:
    """
    Метод возвращает все доступные текстовые модели
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(select(Text.value))
        result = result_data.scalars().all()
    return [company for company in result] if result else []


async def get_all_picture_model() -> list:
    """
    Метод возвращает все доступные модели для генерации изображений
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(select(Picture.value))
        result = result_data.scalars().all()
    return [company for company in result] if result else []


async def insert_new_user(tel_id: int) -> None:
    """
    Метод добавляет нового пользователя в бд
    :param tel_id:
    :return:
    """
    async with get_db_session() as session:
        await session.execute(insert(User).values(tel_id=tel_id))
        await session.commit()
