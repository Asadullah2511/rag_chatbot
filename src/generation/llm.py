from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from config import settings


def get_llm() -> BaseChatModel:
    provider = settings.llm_provider.lower()

    if provider == "anthropic" and settings.anthropic_api_key:
        return ChatAnthropic(
            model=settings.llm_model,
            anthropic_api_key=settings.anthropic_api_key,
            temperature=0.1,
        )

    return ChatOpenAI(
        model=settings.llm_model,
        openai_api_key=settings.openai_api_key,
        temperature=0.1,
    )
