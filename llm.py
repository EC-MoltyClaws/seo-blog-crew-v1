import os
from crewai import LLM


def _get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in .env")
    return api_key


def get_default_llm() -> LLM:
    """GPT-4o — used by all agents."""
    return LLM(
        model="gpt-4o",
        api_key=_get_openai_api_key(),
    )


def get_pro_llm() -> LLM:
    """GPT-4o — used by agents that require higher content quality."""
    return LLM(
        model="gpt-4o",
        api_key=_get_openai_api_key(),
    )
