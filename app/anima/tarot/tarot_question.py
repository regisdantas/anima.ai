import json
import uuid
from app.ai.ai import query_llm
from app.logger import log_error
from app.database.models.history import HistoryRecord
from app.anima.dream.dream_interpreter import split_message

tarot_prompts = {}

with open("app/anima/prompts/tarot.json", "r") as file:
    tarot_prompts["tarot"] = json.load(file)


async def pick_tarot(question: str, history: list[HistoryRecord]) -> dict:
    global tarot_prompts
    result = {}

    prompt = tarot_prompts["tarot"]["question"].format(
        uuid=str(uuid.uuid4()),
        lines=6,
        question=question,
        history="\n\n".join(record.content for record in history),
    )

    with open("logs/prompts.txt", "a") as file:
        file.write(prompt + "\n\n")

    response = await query_llm(prompt)
    if response:
        result["card"] = split_message(response.content)

    prompt = f"""Please, summarise the question and the tarot card bellow. Answer with the summary, only.
    Do not include anything else in the response. Use at most 2 lines. Use same language as in the question.
example:
question: What does the future hold for my career?
card [card name] - [card description] [interpretation] 
question:
{question}
---
tarot card:
{result["card"]}
---
Response:
"""
    response = await query_llm(prompt)
    if response:
        result["summary"] = response.content

    return result
