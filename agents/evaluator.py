from crewai import Agent
from llm import get_default_llm


def build_evaluator_agent():
    return Agent(
        llm=get_default_llm(),
        role="Content Evaluator",
        goal="Review blog posts for quality, accuracy, and SEO before publishing",
        backstory=(
            "You are the last check before a post goes live. "
            "You flag factual errors, weak SEO, or content that doesn't meet WanderPaws standards."
        ),
        tools=[],  # TODO: add evaluation tools
        verbose=True,
    )
