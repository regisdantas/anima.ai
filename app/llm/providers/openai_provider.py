import os
import asyncio
import uuid
from io import BytesIO

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from openai import AsyncOpenAI

from app.logger import log_info, log_error

class OpenAILLMProvider:
    def __init__(self, api_key: str = None, model_name: str = "gpt-4o-mini"):
        if not api_key:
            raise ValueError("API key must be provided for OpenAI provider.")

        self.model_name = model_name
        self.session_id = str(uuid.uuid4())
        self.memory = ChatMessageHistory()
        self.llm = ChatOpenAI(model_name=model_name, openai_api_key=api_key)
        self.client = AsyncOpenAI(api_key=api_key)

    def get_session_history(self, session_id):
        return self.memory

    async def generate_response(self, prompt: str):
        response = await self.llm.ainvoke(prompt)
        return response

    async def generate_tts(self, text: str):
        response = await self.client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text,
            instructions="Fale em português do Brasil.",
        )
        return await response.aread()

    async def transcribe_audio(self, audio_bytes: BytesIO) -> str:
        response = await self.client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=("audio.ogg", audio_bytes, "audio/ogg"),
            language="pt"
        )
        return response.text

async def main():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    llm_instance = OpenAILLMProvider(model_name="gpt-4o-mini", api_key=openai_api_key)

    response = await llm_instance.generate_response("Hello, how are you?")
    print("AI Response:", response)

if __name__ == "__main__":
    asyncio.run(main())
