from crewai import Agent
from tools.web_search import web_search_tool
from llm import get_default_llm


def build_researcher_agent():
    return Agent(
        llm=get_default_llm(),
        role="SEO Content Researcher",
        goal=(
            "Research the assigned topic thoroughly and return at least 2 citable facts or statistics "
            "(APA format) along with key insights tailored to the target audience, "
            "so the writer has everything needed to produce an authoritative blog post."
        ),
        backstory=(
            "You are WanderPaws' dedicated content researcher. Given a topic, category, and target "
            "audience from the Main sheet, you search for relevant facts, expert findings, and "
            "up-to-date statistics. You always surface at least 2 facts that can be cited in APA "
            "style (Author, Year) with full source URLs. You tailor the depth and angle of your "
            "research to the specified audience — whether that's first-time pet travellers, "
            "experienced adventurers, or cat owners exploring harness training."
        ),
        tools=[web_search_tool],
        verbose=True,
    )
