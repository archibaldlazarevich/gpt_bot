import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from src.config.config import BOT_TOKEN, DEFAULT_COMMANDS
from src.handlers.default.start import start_router
from src.handlers.default.help import help_router
from src.handlers.custom.picture import picture_router
from src.middlewares.middleware import Middleware

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def set_commands():
    commands = [
        BotCommand(command=command[0], description=command[1])
        for command in DEFAULT_COMMANDS
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands()


async def main():
    dp.include_routers(start_router, help_router, picture_router)
    dp.startup.register(start_bot)
    dp.message.middleware(Middleware())
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_description(
            "GPT_bot - Это телеграмм-бот, который предоставляет\n"
            "возможности искуственного интелекта по генерации текста,"
            "\nизображений либо аудио по запросу",
            language_code="ru",
        )
        await dp.start_polling(
            bot, allowed_updates=dp.resolve_used_update_types()
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
