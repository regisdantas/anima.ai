import asyncio
from typing import Callable, Any

from app.anima.models.user import User
from app.anima.dream_interpreter import interpret_dream

async def handle_dream(user: User, dream_description: str, callback: Callable[[User, list[str]], None], metadata: Any):
    async def _run():
        try:
            result = await interpret_dream(dream_description, user.get_history())
            await callback(user, result, metadata)
        except Exception as e:
            print("[ERROR] An error occurred:", e)
            await callback(user, ["error: " + str(e)], metadata)
    asyncio.create_task(_run())
