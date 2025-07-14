from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove

from src.database.database_func import update_user_data_text
from src.func.api_func import create_new_text
from src.func.custom_func import send_keyboard, db_error, send_text_message
from src.keyboards.reply import (
    check_new_text_model,
    check_text_rep,
)

text_router = Router()


class Text(StatesGroup):
    init: State = State()
    check: State = State()
    model: State = State()
    res: State = State()


@text_router.message(Command("text"))
async def init_text(message: Message, state: FSMContext):
    await state.clear()
    reply_data = await check_text_rep(tel_id=message.from_user.id)
    if reply_data:
        await state.set_state(Text.init)
        await state.update_data(init=reply_data)
        await message.reply(f'Ваш последний выбор модели ИИ - {reply_data[0]}', reply_markup=ReplyKeyboardRemove())
        await send_keyboard(
            message=message, state=state, state_data=await state.get_state()
        )
    else:
        reply_data = await check_new_text_model()
        if reply_data:
            await state.set_state(Text.check)
            await state.update_data(check=reply_data)
            await send_keyboard(
                message=message, state=state, state_data=await state.get_state()
            )
        else:
            await db_error(message= message, state= state)


@text_router.message(F.text == "Выбрать модель", Text.init)
async def check_model_new(message: Message, state: FSMContext):
    repl_data = await check_new_text_model()
    if repl_data:
        await state.set_state(Text.check)
        await state.update_data(check=repl_data)
        await send_keyboard(
            message=message, state=state, state_data=await state.get_state()
        )
    else:
        await db_error(message= message, state= state)


@text_router.message(F.text == "Оставить старое", Text.init)
@text_router.message(Text.check)
async def create_prompt(message: Message, state: FSMContext):
    if message.text == 'Оставить старое':
        model_data = await state.get_value('init')
        await state.update_data(init=model_data[0])
        await message.reply(
            "Напишите промпт для получения необходимой информации."
            "\nЧем более подробнее вы опишите свои пожелания,тем больше"
            "\nбудет соответсвовать вашим идеям конечные данные.",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(Text.res)
    else:
        data = await state.get_value("check")
        if message.text.lower() in data[0]:
            await state.update_data(init=message.text.lower())
            await message.reply(
                "Напишите промпт для получения необходимой информации."
                "\nЧем более подробнее вы опишите свои пожелания,тем больше"
                "\nбудет соответсвовать вашим идеям конечные данные.",
                reply_markup=ReplyKeyboardRemove(),
            )
            await state.set_state(Text.res)
        else:
            await message.reply(
                "Пожалуйста, выберите данные из клавиатуры.",
                reply_markup=ReplyKeyboardRemove(),
            )
            await send_keyboard(
                message=message, state=state, state_data=await state.get_state()
            )


@text_router.message(Text.res)
async def create_text(message: Message, state: FSMContext):
    model = await state.get_value("init")
    await update_user_data_text(tel_id= message.from_user.id, text_model=model)
    result = await create_new_text(text=message.text, model=model)
    await message.answer(
        "Результат генерации:", reply_markup=ReplyKeyboardRemove()
    )
    await send_text_message(message=message, text= result)
    await state.clear()
