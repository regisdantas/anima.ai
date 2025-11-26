import json
from app.llm.llm_factory import get_llm

prompts = {}

with open("app/anima/prompts/jung.json", "r") as file:
    prompts['jung'] = json.load(file)

async def interpret_dream(dream_description: str) -> str:
    global prompts
    llm = get_llm()
    prompt = f"{prompts['jung']['system-prompt']}\n\nUser Input:\n{dream_description}\n"
    response = await llm.generate_response(prompt)
    return response.content
