from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

screen_data = [
    'samsung_a40', '1280_1024', '1366_768', '1440_900', '1600_900', '1680_1050',
    '1920_1080', '1920_1200', '2560_1080', '2560_1440', '3440_1440', '3840_2160',
    '4096_2160', '5120_2880',
]

async def solution_data():
    """
    Метод для формарования клавиатуры для выбора разрешения монитора
    :return:
    """
    keyboard = ReplyKeyboardBuilder()
    for data in screen_data:
        keyboard.add(KeyboardButton(text=data))
    markup = keyboard.adjust(1).as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return screen_data, markup

async def check_monitor(tel_id: int):
    """
    Метод для отправки клавиатуры при на начилие записей о пользователе в базе данных
    :param tel_id:
    :return:
    """