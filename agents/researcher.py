from crewai import Agent
from tools.web_search import web_search_tool
from llm import get_default_llm


def build_researcher_agent():
    return Agent(
        llm=get_default_llm(),
        role="SEO Researcher",
        goal="Find accurate, up-to-date information on pet travel topics",
        backstory=(
            "You research pet travel topics for WanderPaws blog posts. "
            "You gather facts, statistics, and key points that the writer will turn into an article."
        ),
        tools=[web_search_tool],
        verbose=True,
    )
