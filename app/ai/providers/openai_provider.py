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
        self.llm = ChatOpenAI(model_name=model_name, openai_api_key=api_key, temperature=1)

    def get_session_history(self, session_id):
        return self.memory

    async def generate_response(self, prompt: str):
        response = await self.llm.ainvoke(prompt)
        return response

class IOpenAISpeechProvider:
    def __init__(self, api_key: str = None, model_config: dict = {"tts": "gpt-4o-mini-tts", "transcribe": "gpt-4o-mini-transcribe"}):
        if not api_key:
            raise ValueError("API key must be provided for OpenAI provider.")

        self.model_config = model_config
        self.session_id = str(uuid.uuid4())
        self.memory = ChatMessageHistory()
        self.llm = ChatOpenAI(model_name=model_config["tts"], openai_api_key=api_key, temperature=1)
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_tts(self, text: str, voice: str = "alloy", language: str = "pt_BR") -> BytesIO:
        response = await self.client.audio.speech.create(
            model=self.model_config["tts"],
            voice=voice,
            input=text,
            instructions=f"Speack in {language}.",
        )
        return await response.aread()

    async def transcribe_audio(self, audio_bytes: BytesIO) -> str:
        response = await self.client.audio.transcriptions.create(
            model=self.model_config["transcribe"],
            file=("audio.ogg", audio_bytes, "audio/ogg"),
            language="pt_BR"
        )
        return response.text

