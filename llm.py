import os
from crewai import LLM


def get_default_llm(verbose: bool = True) -> LLM:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in .env")

    return LLM(
        model="gemini/gemini-2.5-flash",
        api_key=api_key,
        verbose=verbose,
    )
