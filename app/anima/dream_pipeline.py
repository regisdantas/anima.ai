import asyncio
from typing import Callable, Any

from app.anima.models.user import User

async def handle_dream(user: User, dream_description: str, callback: Callable[[User, str], None], metadata: Any):
    async def _run():
        try:
            result = "Hello, nice try"
            await callback(user, result, metadata)
        except Exception as e:
            print("[ERROR] An error occurred:", e)
            await callback(user, "error: " + str(e), metadata)
    asyncio.create_task(_run())
