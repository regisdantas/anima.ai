import os
import asyncio
import uuid

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory

class OpenAILLMProvider:
    def __init__(self, api_key: str = None, model_name: str = "gpt-4o-mini"):
        if not api_key:
            raise ValueError("API key must be provided for OpenAI provider.")

        self.model_name = model_name
        self.session_id = str(uuid.uuid4())
        self.memory = ChatMessageHistory()
        self.llm = ChatOpenAI(model_name=model_name, openai_api_key=api_key)

    def get_session_history(self, session_id):
        return self.memory

    async def generate_response(self, prompt: str):
        response = await self.llm.ainvoke(prompt)
        return response

async def main():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    llm_instance = OpenAILLMProvider(model_name="gpt-4o-mini", api_key=openai_api_key)

    response = await llm_instance.generate_response("Hello, how are you?")
    print("AI Response:", response)

if __name__ == "__main__":
    asyncio.run(main())
