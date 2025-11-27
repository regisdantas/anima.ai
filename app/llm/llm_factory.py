import os
from dotenv import load_dotenv
from app.llm.providers.openai_provider import OpenAILLMProvider

_llm_instance = None

def get_llm():
    global _llm_instance

    if _llm_instance is None:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        _llm_instance = OpenAILLMProvider(
            model_name=model_name,
            api_key=api_key,
        )

    return _llm_instance
