from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.config.config import DEFAULT_COMMANDS

start_router = Router()


@start_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await state.clear()
    commands = "\n".join(
        [f"/{command[0]} - {command[1]}" for command in DEFAULT_COMMANDS]
    )
    await message.reply(
        f"Бот с интеграцияей API 'pollinations.ai'.\n"
        f"Команды, которые вы можете использовать:\n"
        f"{commands}",
        reply_markup=ReplyKeyboardRemove(),
    )
