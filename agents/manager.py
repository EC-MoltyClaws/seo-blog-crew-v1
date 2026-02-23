from crewai import Agent
from tools.make_webhook import get_make_mcp_server
from llm import get_default_llm


def build_manager_agent():
    return Agent(
        llm=get_default_llm(),
        role="Blog Manager",
        goal="Coordinate the blog production pipeline from topic to publish",
        backstory=(
            "You oversee the full blog production process for WanderPaws. "
            "You delegate research, writing, and publishing tasks to the right agents "
            "and trigger Make.com workflows to publish the final post."
        ),
        mcps=[get_make_mcp_server()],
        verbose=True,
    )
