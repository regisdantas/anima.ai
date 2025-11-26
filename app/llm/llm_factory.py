import os
from dotenv import load_dotenv
from app.llm.providers.openai_provider import OpenAILLMProvider

_llm_instance = None

def get_llm():
    global _llm_instance

    if _llm_instance is None:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        _llm_instance = OpenAILLMProvider(
            model_name="gpt-5.1",
            api_key=api_key,
        )

    return _llm_instance
