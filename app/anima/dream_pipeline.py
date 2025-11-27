import asyncio
from typing import Callable, Any

from app.logger import log_info, log_error
from app.database.models.user import User
from app.anima.dream_interpreter import interpret_dream

async def handle_dream(user: User, dream_description: str, callback: Callable[[User, list[str]], None], metadata: Any):
    async def _run():
        retries = 3
        while retries > 0:
            try:
                result = await interpret_dream(dream_description, user.get_history())
                break
            except Exception as e:
                log_error("[ERROR] An error occurred:", e)
                retries -= 1

        await callback(user, result, metadata)

    asyncio.create_task(_run())
