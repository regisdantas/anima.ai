import json
import uuid
from app.llm.llm_factory import get_llm

prompts = {}

with open("app/anima/prompts/jung.json", "r") as file:
    prompts['jung'] = json.load(file)

async def interpret_dream(dream_description: str) -> str:
    global prompts
    final_response = []
    current_response = ""
    llm = get_llm()
    for topic in prompts['jung']['topics']:
        print(topic)
        prompt = prompts['jung']["interpretation_prompt"].format(uuid=str(uuid.uuid4()),
                                                                 lines=3,
                                                                 current_topic=topic,
                                                                 dream_description=dream_description,
                                                                 history="",
                                                                 current_response=current_response)
        response = await llm.generate_response(prompt)
        current_response += f"# {topic}\n{response.content}\n"
        final_response.append(response.content)
    return final_response
