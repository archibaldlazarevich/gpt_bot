from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove


async def send_keyboard(
    message: Message, state: FSMContext, state_data: str
) -> None:
    """
    Метод для отправки корректной клавиатуры
    :param state_data: текущее состояние в текстовом виде
    :param message: сообщение пользователя
    :param state: состояние
    :return:
    """
    state_data = state_data.split(sep=":")[1]
    reply_data = await state.get_value(state_data)
    if reply_data:
        await message.answer(
            "Выберите данные из списка", reply_markup=reply_data[1]
        )
    else:
        await state.clear()
        await message.answer(
            "Ошибка в работе Бота.", reply_markup=ReplyKeyboardRemove()
        )


async def db_error(message: Message, state: FSMContext) -> None:
    """
    Метод для отправки сообщения об ошибке в базе данных
    :param message: сообщение пользователя
    :param state: состояние
    :return:
    """
    await state.clear()
    await message.answer(
        "Ошибка в работе базы данных", reply_markup=ReplyKeyboardRemove()
    )


async def send_text_message(message: Message, text: str) -> None:
    """
    Метод для отправки текста в сообщениях длиной не более 4096 единиц
    :param text: текстовое сообщение
    :param message: сообщение пользователя
    :return:
    """
    for i in range(0, len(text), 4096):
        await message.answer(text[i : i + 4096])  # noqa: E203
