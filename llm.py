import os
from crewai import LLM


def _get_gemini_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in .env")
    return api_key


def get_default_llm(verbose: bool = True) -> LLM:
    """Gemini 2.5 Flash — used by most agents."""
    return LLM(
        model="gemini/gemini-2.5-flash",
        api_key=_get_gemini_api_key(),
        verbose=verbose,
    )


def get_pro_llm(verbose: bool = True) -> LLM:
    """Gemini 2.5 Pro — used by agents that require higher content quality."""
    return LLM(
        model="gemini/gemini-2.5-pro",
        api_key=_get_gemini_api_key(),
        verbose=verbose,
    )
