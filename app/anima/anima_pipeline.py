import asyncio
from typing import Callable, Any

from app.logger import log_error
from app.database.models.user import User
from app.anima.dream.dream_interpreter import interpret_dream
from app.anima.tarot.tarot_question import pick_tarot
from app.database.models.history import HistoryRecord


async def handle_dream(
    user: User,
    dream_description: str,
    history: list[HistoryRecord],
    callback: Callable[[User, list[str]], None],
    metadata: Any,
):
    async def _run():
        retries = 3
        while retries > 0:
            try:
                result = await interpret_dream(dream_description, history)
                break
            except Exception as e:
                log_error("[ERROR] An error occurred:", e)
                retries -= 1

        await callback(user, result, metadata)

    asyncio.create_task(_run())


async def handle_tarot_pipeline(
    user: User,
    question: str,
    history: list[HistoryRecord],
    callback: Callable[[User, list[str]], None],
    metadata: Any,
):
    async def _run():
        retries = 3
        while retries > 0:
            try:
                result = await pick_tarot(question, history)
                break
            except Exception as e:
                log_error("[ERROR] An error occurred:", e)
                retries -= 1

        await callback(user, result, metadata)

    asyncio.create_task(_run())
