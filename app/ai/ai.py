import os
from dotenv import load_dotenv
from app.ai.providers.openai_provider import OpenAILLMProvider, IOpenAISpeechProvider

_ai_instances = None

def get_ai():
    global _ai_instances

    if _ai_instances is None:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")

        _ai_instances = {
            "llm": OpenAILLMProvider(model_name=os.getenv("OPENAI_LLM_MODEL", "gpt-4o-mini"), api_key=api_key),
            "speech": IOpenAISpeechProvider(api_key=api_key, model_config={
                "tts": os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
                "transcribe": os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe")
            })
        }

    return _ai_instances

