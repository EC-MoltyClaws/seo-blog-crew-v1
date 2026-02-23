from crewai import Agent
from tools.make_webhook import get_latest_topic, publish_blog_post
from llm import get_default_llm


def build_publisher_agent():
    return Agent(
        llm=get_default_llm(),
        role="Blog Publisher",
        goal=(
            "Retrieve the next unwritten blog topic from the Main Google Sheet via Make.com, "
            "and after the post is approved, publish it via Make.com and update the sheet "
            "with the post URL, publication date, and written-by details."
        ),
        backstory=(
            "You are WanderPaws' publishing specialist. You handle all Make.com interactions. "
            "You have two tools: 'Get Latest Unwritten Blog Topic' which fetches the next topic, "
            "and 'Publish Blog Post to Shopify' which publishes the approved content to the website "
            "and updates the Google Sheet."
        ),
        tools=[get_latest_topic, publish_blog_post],
        verbose=True,
    )
