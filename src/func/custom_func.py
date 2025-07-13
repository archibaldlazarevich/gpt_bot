from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove


async def send_keyboard(message: Message, state: FSMContext, state_data: str):
    """
    Метод для отправки корректной клавиатуры
    :param message:
    :param state:
    :param sate_data:
    :return:
    """
    reply_data = await state.get_value(state_data)
    if reply_data:
        await message.reply('Выберите данные из списка', reply_markup=reply_data[1])
    else:
        await state.clear()
        await message.reply('Ошибка в работе Бота.', reply_markup=ReplyKeyboardRemove())
