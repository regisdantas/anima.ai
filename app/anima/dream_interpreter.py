import json
import uuid
from app.ai.ai import get_ai
from app.bot.utils.format_utils import split_message

prompts = {}

with open("app/anima/prompts/jung.json", "r") as file:
    prompts['jung'] = json.load(file)

async def interpret_dream(dream_description: str, history: str) -> str:
    global prompts
    ai = get_ai()
    retries = 3
    while retries > 0:
        try:
            prompt = prompts['jung']["interpretation_prompt"].format(uuid=str(uuid.uuid4()),
                                                             lines=20,
                                                             dream_description=dream_description,
                                                             history="")
            response = await ai["llm"].generate_response(prompt)
            break
        except Exception as e:
            retries -= 1
            if retries == 0:
                raise e
    return split_message(response.content)

