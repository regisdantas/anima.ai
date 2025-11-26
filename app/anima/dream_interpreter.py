import json
from app.llm.llm_factory import get_llm

with open("app/anima/prompts/jung.json", "r") as file:
    prompts = json.load(file)

async def interpret_dream(dream_description: str) -> str:
    global prompts
    llm = get_llm()
    prompt = f"{prompts['system-prompt']}\n\nUser Input:\n{dream_description}\n"
    response = await llm.generate_response(prompt)
    return response.content
