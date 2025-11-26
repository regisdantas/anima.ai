import json
import uuid
from app.llm.llm_factory import get_llm
from app.bot.utils.format_utils import split_message

prompts = {}

with open("app/anima/prompts/jung.json", "r") as file:
    prompts['jung'] = json.load(file)

async def interpret_dream(dream_description: str, history: str) -> str:
    global prompts
    llm = get_llm()
    retries = 3
    while retries > 0:
        try:
            prompt = prompts['jung']["interpretation_prompt"].format(uuid=str(uuid.uuid4()),
                                                             lines=20,
                                                             dream_description=dream_description,
                                                             history="")
            response = await llm.generate_response(prompt)
            break
        except Exception as e:
            retries -= 1
            if retries == 0:
                raise e
    return split_message(response.content)

