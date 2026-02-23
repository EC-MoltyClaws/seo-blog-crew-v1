from crewai import Agent
from llm import get_default_llm


def build_html_writer_agent():
    return Agent(
        llm=get_default_llm(),
        role="HTML Writer",
        goal="Convert blog drafts into clean, publish-ready HTML",
        backstory=(
            "You take the finished blog draft and format it as valid HTML "
            "ready for Shopify. You add headings, lists, and semantic markup."
        ),
        tools=[],
        verbose=True,
    )
