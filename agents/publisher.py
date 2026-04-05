from crewai import Agent
from tools.make_webhook import get_latest_topic, publish_blog_post
from llm import get_default_llm


def build_publisher_agent():
    return Agent(
        llm=get_default_llm(),
        role="Blog Publisher",
        goal=(
            "Retrieve the next unwritten blog topic from the GitHub Issues queue, "
            "and after the post is approved and formatted, publish it to Shopify."
        ),
        backstory=(
            "You are WanderPaws' publishing specialist. You handle all system integrations. "
            "You have two tools: 'Get Latest Unwritten Blog Topic' which fetches the next topic from GitHub, "
            "and 'Publish Blog Post to Shopify' which publishes the approved content to the website "
            "and automatically closes the issue."
        ),
        tools=[get_latest_topic, publish_blog_post],
        verbose=True,
    )
