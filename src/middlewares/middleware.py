import time
from typing import Any, Awaitable, Callable, Dict, cast

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, Update


class Middleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        message = cast(Message, event)

        state = data.get("state")
        assert state is not None
        state_data = await state.get_state()
        text = message.text or ""
        if text.startswith("/") and state_data is not None:
            await state.clear()
            dp = data.get("dispatcher")
            assert dp is not None
            bot = data.get("bot")
            assert bot is not None
            update_id = data.get("update_id")
            if update_id is None:
                update_id = int(time.time() * 1000)

            update = Update(update_id=update_id, message=message)
            if dp:
                await dp.feed_update(bot=bot, update=update)
                return None

        return await handler(message, data)
