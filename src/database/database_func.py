from sqlalchemy.future import select

from src.database.create_db import get_db_session
from src.database.models import User


async def check_text_data(tel_id: int):
    """
    Метод для проверки данных о text models data пользователя
    :param tel_id:
    :return:
    """

    async with get_db_session() as session:
        result_data = await session.execute(select(User.text).where(User.tel_id == tel_id))
        result = result_data.scalar_one_or_none
    return result if result else None


async def check_monitor_data(tel_id: int):
    """
    Метод для проверки данных о monitor models data пользователя
    :param tel_id:
    :return:
    """

    async with get_db_session() as session:
        result_data = await session.execute(select(User.monitor).where(User.tel_id == tel_id))
        result = result_data.scalar_one_or_none
    return result if result else None

async def check_picture_data(tel_id: int):
    """
    Метод для проверки данных о monitor models data пользователя
    :param tel_id:
    :return:
    """

    async with get_db_session() as session:
        result_data = await session.execute(select(User.picture).where(User.tel_id == tel_id))
        result = result_data.scalar_one_or_none
    return result if result else None