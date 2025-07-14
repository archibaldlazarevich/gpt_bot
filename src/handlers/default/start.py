from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.config.config import DEFAULT_COMMANDS
from src.database.database_func import insert_new_user

start_router = Router()


@start_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await state.clear()
    assert message.from_user is not None
    commands = "\n".join(
        [f"/{command[0]} - {command[1]}" for command in DEFAULT_COMMANDS]
    )
    await message.reply(
        f"Бот с интеграцияей API 'pollinations.ai'.\n"
        f"Команды, которые вы можете использовать:\n"
        f"{commands}",
        reply_markup=ReplyKeyboardRemove(),
    )
    await insert_new_user(message.from_user.id)
