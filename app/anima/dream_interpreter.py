import json
import uuid
from app.ai.ai import get_ai
from app.bot.utils.format_utils import split_message
from app.logger import log_error
from app.database.models.history import HistoryRecord

prompts = {}

with open("app/anima/prompts/jung.json", "r") as file:
    prompts["jung"] = json.load(file)


async def query_llm(prompt: str, retries: int = 3):
    ai = get_ai()
    retries = 3
    while retries > 0:
        try:
            response = await ai["llm"].generate_response(prompt)
            break
        except Exception as e:
            log_error("[ERROR] An error occurred:", e)
            retries -= 1
            if retries == 0:
                return None

    return response


async def interpret_dream(
    dream_description: str, history: list[HistoryRecord] = []
) -> str:
    global prompts
    result = {}

    prompt = prompts["jung"]["interpretation_prompt"].format(
        uuid=str(uuid.uuid4()),
        lines=20,
        dream_description=dream_description,
        history="\n\n".join(record.content for record in history),
    )

    with open("logs/prompts.txt", "a") as file:
        file.write(prompt + "\n\n")

    response = await query_llm(prompt)
    if response:
        result["interpretation"] = split_message(response.content)

    prompt = f"""Please, summarise the description and interpretation of the dream bellow. Answer with the summary, only.
    Do not include anything else in the response. Use at most 10 lines. Use same language as in the description.
dream_description:
{dream_description}
---
interpretation:
{result["interpretation"]}
---
Response:
"""
    response = await query_llm(prompt)
    if response:
        result["summary"] = response.content

    return result
