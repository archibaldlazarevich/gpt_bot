import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, Message, ReplyKeyboardRemove

from src.func.api_func import create_new_audio

audio_router = Router()


class Audio(StatesGroup):
    init: State = State()


@audio_router.message(Command("audio"))
async def init_audio(message: Message, state: FSMContext):
    await state.clear()
    await message.reply(
        "Напишите промпт для получения необходимой информации."
        "\nЧем более подробнее вы опишите свои пожелания,тем больше"
        "\nбудет соответсвовать вашим идеям конечные данные.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Audio.init)


@audio_router.message(Audio.init)
async def create_audio(message: Message, state: FSMContext):
    assert message.text is not None
    assert message.from_user is not None
    await state.clear()
    if await create_new_audio(user_id=message.from_user.id, text=message.text):
        await message.answer(
            "Результат генерации:", reply_markup=ReplyKeyboardRemove()
        )
        file = FSInputFile(
            path=(f"{message.from_user.id}.mp3"),
            filename=f"{message.from_user.id}.mp3",
        )
        await message.reply_audio(audio=file)
        os.remove(f"{message.from_user.id}.mp3")
    else:
        await message.answer(
            "Выберите другую модель ИИ, с текущей возникли проблемы.",
            reply_markup=ReplyKeyboardRemove(),
        )
