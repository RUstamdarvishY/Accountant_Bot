from typing import Any, Awaitable, Callable, Dict, Optional
from aiogram import BaseMiddleware
from aiogram.dispatcher.handler import HandlerObject
from aiogram.types import TelegramObject, User
from aiolimiter import AsyncLimiter


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, default_rate: float = 0.1):
        self.limiters: Dict[str, AsyncLimiter] = {}
        self.default_rate = default_rate

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: Dict[str, Any]):
        user: Optional[User] = data.get("event_from_user")
        real_handler: HandlerObject = data["handler"]
        throttling_key = getattr(
            real_handler, "throttling_key", f"{real_handler.callback}"
        )
        throttling_rate = getattr(
            real_handler, "throttling_rate", self.default_rate)
        if not user:
            return await handler(event, data)
        limiter = self.limiters.setdefault(
            f"{user.id}:{throttling_key}", AsyncLimiter(1, throttling_rate))
        if limiter.has_capacity():
            async with limiter:
                return await handler(event, data)
