from crewai import Agent
from llm import get_default_llm


def build_writer_agent():
    return Agent(
        llm=get_default_llm(),
        role="Blog Writer",
        goal="Write engaging, SEO-optimised blog posts for WanderPaws",
        backstory=(
            "You turn research notes into clear, friendly blog posts aimed at pet owners "
            "who travel with their animals. You write in plain English and follow SEO best practices."
        ),
        tools=[],
        verbose=True,
    )
