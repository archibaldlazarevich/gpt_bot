from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import (
    InlineKeyboardMarkup,
    ReplyKeyboardBuilder,
    ReplyKeyboardMarkup,
)

from src.database.database_func import (
    check_monitor_data,
    check_picture_data,
    check_text_data,
    get_all_picture_model,
    get_all_text_model,
)

screen_data: list = [
    "samsung_a40_1080x2340",
    "1280_1024",
    "1366_768",
    "1440_900",
    "1600_900",
    "1680_1050",
    "1920_1080",
    "1920_1200",
    "2560_1080",
    "2560_1440",
    "3440_1440",
    "3840_2160",
    "4096_2160",
    "5120_2880",
]


async def solution_data() -> (
    tuple[list, InlineKeyboardMarkup | ReplyKeyboardMarkup]
):
    """
    Метод для формирования клавиатуры для выбора разрешения монитора
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


async def check_monitor_rep(
    tel_id: int,
) -> tuple[str, InlineKeyboardMarkup | ReplyKeyboardMarkup] | None:
    """
    Метод для отправки клавиатуры при на наличие
     записей о пользователе в базе данных
    :param tel_id: id телеграмм пользователя
    :return:
    """
    result_data = await check_monitor_data(tel_id=tel_id)
    if result_data:
        all_data = ["Оставить старое", "Выбрать разрешение"]
        keyboard = ReplyKeyboardBuilder()
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return result_data, markup
    return None


async def check_picture_rep(
    tel_id: int,
) -> tuple[str, InlineKeyboardMarkup | ReplyKeyboardMarkup] | None:
    """
    Метод для отправки клавиатуры при на
     наличие записей о пользователе в базе данных
    :param tel_id: id телеграмм пользователя
    :return:
    """
    result_data = await check_picture_data(tel_id=tel_id)
    if result_data:
        all_data = ["Оставить старое", "Выбрать модель"]
        keyboard = ReplyKeyboardBuilder()
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return result_data, markup
    return None


async def check_text_rep(
    tel_id: int,
) -> tuple[str, InlineKeyboardMarkup | ReplyKeyboardMarkup] | None:
    """
    Метод для отправки клавиатуры при на
    наличие записей о пользователе в базе данных
    :param tel_id: id телеграмм пользователя
    :return:
    """
    result_data = await check_text_data(tel_id=tel_id)
    if result_data:
        all_data = ["Оставить старое", "Выбрать модель"]
        keyboard = ReplyKeyboardBuilder()
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return result_data, markup
    return None


async def check_new_text_model() -> (
    tuple[list, InlineKeyboardMarkup | ReplyKeyboardMarkup] | None
):
    """
    Метод, формирует клавиатуру с наличием доступных текстовых моделей
    :return:
    """
    all_data = await get_all_text_model()
    if all_data:
        keyboard = ReplyKeyboardBuilder()
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return None


async def monitor_nodel_rep() -> (
    tuple[list, InlineKeyboardMarkup | ReplyKeyboardMarkup] | None
):
    """
    Метод для формирования клавитуры со всеми доступными
     моделями для генерации изображений
    :return:
    """
    all_data = await get_all_picture_model()
    if all_data:
        keyboard = ReplyKeyboardBuilder()
        for data in all_data:
            keyboard.add(KeyboardButton(text=data))
        markup = keyboard.adjust(1).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        return all_data, markup
    return None
