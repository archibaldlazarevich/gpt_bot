import os
from typing import cast

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardMarkup, ReplyKeyboardMarkup

from src.database.database_func import (
    get_resolution_w_h,
    update_user_data_picture,
)
from src.func.api_func import create_new_picture
from src.func.custom_func import db_error, send_keyboard
from src.keyboards.reply import (
    check_monitor_rep,
    check_picture_rep,
    monitor_nodel_rep,
    solution_data,
)

picture_router = Router()


class Picture(StatesGroup):
    init: State = State()
    check: State = State()
    model: State = State()
    new_model: State = State()
    res: State = State()


@picture_router.message(Command("picture"))
async def init_picture(message: Message, state: FSMContext):
    assert message.from_user is not None
    await state.clear()
    reply_data = await check_monitor_rep(tel_id=message.from_user.id)
    if reply_data:
        await state.set_state(Picture.init)
        await state.update_data(init=reply_data)
        await message.reply(
            f"Последнее используемое вами разрешение - {reply_data[0]}",
            reply_markup=ReplyKeyboardRemove(),
        )
        state_data: str = cast(str, await state.get_state())
        await send_keyboard(
            message=message, state=state, state_data=state_data
        )
    else:
        reply_data_new: (
            tuple[list, InlineKeyboardMarkup | ReplyKeyboardMarkup] | None
        ) = await solution_data()
        await message.reply(
            "Выберите подходящее для вас разрешение изображения.",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(Picture.check)
        await state.update_data(check=reply_data_new)
        state_data_new: str = cast(str, await state.get_state())
        await send_keyboard(
            message=message, state=state, state_data=state_data_new
        )


@picture_router.message(F.text == "Выбрать разрешение", Picture.init)
async def check_picture_if_new(message: Message, state: FSMContext):
    assert message.from_user is not None
    repl_data = await solution_data()
    await state.set_state(Picture.check)
    await state.update_data(check=repl_data)
    state_data: str = cast(str, await state.get_state())
    await send_keyboard(message=message, state=state, state_data=state_data)


async def send_model_res(message: Message, state: FSMContext):
    assert message.from_user is not None
    reply_data = await check_picture_rep(tel_id=message.from_user.id)
    if reply_data:
        await state.set_state(Picture.model)
        await state.update_data(model=reply_data)
        await message.reply(
            f"Последняя используемая вами модель ИИ - {reply_data[0]}",
            reply_markup=ReplyKeyboardRemove(),
        )
        state_data: str = cast(str, await state.get_state())
        await send_keyboard(
            message=message, state=state, state_data=state_data
        )
    else:
        reply_data_new: (
            tuple[list, InlineKeyboardMarkup | ReplyKeyboardMarkup] | None
        ) = await monitor_nodel_rep()
        if reply_data_new:
            await state.set_state(Picture.new_model)
            await state.update_data(new_model=reply_data_new)
            await message.reply(
                "Выберите подходящюю модель ИИ для генерации изображений.",
                reply_markup=ReplyKeyboardRemove(),
            )
            state_data_new: str = cast(str, await state.get_state())
            await send_keyboard(
                message=message,
                state=state,
                state_data=state_data_new,
            )
        else:
            await db_error(message=message, state=state)


@picture_router.message(F.text == "Оставить старое", Picture.init)
@picture_router.message(Picture.check)
async def model_picture(message: Message, state: FSMContext):
    assert message.from_user is not None
    assert message.text is not None
    if message.text == "Оставить старое":
        resolution_data: list = cast(list, await state.get_value("init"))
        await state.update_data(init=resolution_data[0])
        await send_model_res(message=message, state=state)
    else:
        data: list = cast(list, await state.get_value("check"))
        if message.text.lower() in data[0]:
            await state.update_data(init=message.text.lower())
            await send_model_res(message=message, state=state)
        else:
            state_data: str = cast(str, await state.get_state())
            await message.reply(
                "Пожалуйста, выберите данные из клавиатуры.",
                reply_markup=ReplyKeyboardRemove(),
            )
            await send_keyboard(
                message=message,
                state=state,
                state_data=state_data,
            )


@picture_router.message(F.text == "Выбрать модель", Picture.model)
async def change_model(message: Message, state: FSMContext):
    assert message.from_user is not None
    reply_data = await monitor_nodel_rep()
    if reply_data:
        await state.set_state(Picture.new_model)
        await state.update_data(new_model=reply_data)
        await message.reply(
            "Выберите подходящюю модель ИИ для генерации изображений.",
            reply_markup=ReplyKeyboardRemove(),
        )
        state_data: str = cast(str, await state.get_state())
        await send_keyboard(
            message=message, state=state, state_data=state_data
        )
    else:
        await db_error(message=message, state=state)


@picture_router.message(Picture.new_model)
async def create_prompt_old_new_model(message: Message, state: FSMContext):
    assert message.from_user is not None
    assert message.text is not None
    data: list = cast(list, await state.get_value("new_model"))
    if message.text in data[0]:
        await state.update_data(model=message.text)
        await message.reply(
            "Напишите промпт для создания изображения."
            "\nЧем более подробнее вы опишите свои пожелания,тем больше"
            "\nбудет соответсвовать вашим идеям конечное изображение.",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(Picture.res)
    else:
        state_data: str = cast(str, await state.get_state())
        await message.reply(
            "Пожалуйста, выберите данные из клавиатуры.",
            reply_markup=ReplyKeyboardRemove(),
        )
        await send_keyboard(
            message=message, state=state, state_data=state_data
        )


@picture_router.message(F.text == "Оставить старое", Picture.model)
async def create_prompt_old(message: Message, state: FSMContext):
    assert message.from_user is not None
    data: list = cast(list, await state.get_value("model"))
    await state.update_data(model=data[0])
    await message.reply(
        "Напишите промпт для создания изображения."
        "\nЧем более подробнее вы опишите свои пожелания,тем больше"
        "\nбудет соответсвовать вашим идеям конечное изображение.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Picture.res)


@picture_router.message(Picture.res)
async def create_picture(message: Message, state: FSMContext):
    assert message.from_user is not None
    assert message.text is not None
    model_data: str = cast(str, await state.get_value("model"))
    res_data: str = cast(str, await state.get_value("init"))
    await state.clear()
    res_h_w: tuple = cast(tuple, await get_resolution_w_h(res=res_data))
    await update_user_data_picture(
        tel_id=message.from_user.id, res=res_data, model=model_data
    )
    if await create_new_picture(
        user_id=message.from_user.id,
        text=message.text,
        res=res_h_w,
        model=model_data,
    ):
        await message.answer(
            "Результат генерации:", reply_markup=ReplyKeyboardRemove()
        )
        file = FSInputFile(
            path=(f"{message.from_user.id}.png"),
            filename=f"{message.from_user.id}.png",
        )
        await message.reply_animation(animation=file)
        os.remove(f"{message.from_user.id}.png")
    else:
        await message.reply(
            "Выберите другую модель ИИ, с текущей возникли проблемы.",
            reply_markup=ReplyKeyboardRemove(),
        )
