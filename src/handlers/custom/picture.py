import os

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile

from src.func.api_func import create_new_picture
from src.func.custom_func import send_keyboard
from src.keyboards.reply import screen_data

picture_router = Router()



class Picture(StatesGroup):
    init: State = State()
    model: State = State()
    res: State = State()

@picture_router.message(Command('picture'))
async def init_picture(message: Message, state: FSMContext):
    await state.clear()
    repl_data = await screen_data
    await state.set_state(Picture.init)
    await state.update_data(init = repl_data)
    await send_keyboard(message= message, state=state, state_data= await state.get_state())


@picture_router.message(Picture.init)
async def create_prompt(message: Message, state: FSMContext):
    data = await state.get_value('init')
    if message.text in data[0]:
        await state.update_data(init= message.text)
        await message.reply('Напишите промпт для создания изображения.'
                            '\nЧем более подробнее вы опишите свои пожелания,тем больше'
                            '\nбудет соответсвовать вашим идеям конечное изображение.',
                            reply_markup=ReplyKeyboardRemove())
        await state.set_state(Picture.res)
    else:
        await message.reply('Пожалуйста, выберите данные из клавиатуры.', reply_markup=ReplyKeyboardRemove())
        await send_keyboard(message= message, state=state, state_data= await state.get_state())


@picture_router.message(Picture.res)
async def create_picture(message: Message, state: FSMContext):
    res_data = await state.get_value('init')
    await create_new_picture(user_id = message.from_user.id, text= message.text, res= res_data)
    await message.answer('Результат генерации:', reply_markup=ReplyKeyboardRemove())
    file = FSInputFile(
        path=(f"{message.from_user.id}.png"), filename=f"{message.from_user.id}.png"
    )
    await message.reply_animation(animation=file)
    await state.clear()
    os.remove(f"{message.from_user.id}.png")
