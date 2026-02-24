from datetime import datetime
from crewai import Agent, Crew, Process, Task
from llm import get_default_llm
from tools.make_webhook import get_latest_topic, publish_blog_post


def check_publish_pipeline():
    """
    Fetches the real latest topic then immediately publishes a dummy post using
    the fields from that response (blogId, shopify_image_url).

    This catches field-name mismatches between what get_latest_topic returns
    and what publish_blog_post expects — the most likely source of inconsistencies
    in the publish pipeline.
    """
    today = datetime.now().strftime("%m/%d/%Y 9:00 AM")

    publisher = Agent(
        llm=get_default_llm(verbose=False),
        role="Blog Publisher",
        goal="Fetch the latest topic and publish a test post using the data from that response.",
        backstory=(
            "You are a publishing pipeline tester. You have two tools: one to fetch the latest "
            "topic, and one to publish a post. Your job is to call both in sequence and report "
            "the full response from each tool."
        ),
        tools=[get_latest_topic, publish_blog_post],
        verbose=True,
    )

    task = Task(
        description=(
            "Run the full publish handoff in two steps:\n\n"
            "Step 1: Call the 'Get Latest Unwritten Blog Topic' tool. "
            "From the response, extract: blogId and shopify_image_url.\n\n"
            "Step 2: Call the 'Publish Blog Post to Shopify' tool with these values:\n"
            "- blogTitle: 'TEST POST — Pipeline Check (Do Not Publish)'\n"
            "- blogBodyHtml: '<h1>Test Post</h1><p>This is a dummy post used to verify the publish pipeline.</p>'\n"
            "- summaryHtml: '<p>Dummy post for pipeline verification. Safe to ignore.</p>'\n"
            "- blogUrlHandle: 'test-pipeline-check-do-not-publish'\n"
            f"- blogPublishDate: '{today}'\n"
            "- tags: 'test, pipeline-check'\n"
            "- blogID: the blogId from Step 1\n"
            "- skillVersion: 'v1-test'\n"
            "- imageUrl: the shopify_image_url from Step 1 (omit if not present)\n\n"
            "Report the full raw response from both tool calls."
        ),
        expected_output=(
            "The full raw response from the fetch topic tool call, "
            "followed by the full raw response from the publish tool call."
        ),
        agent=publisher,
    )

    crew = Crew(agents=[publisher], tasks=[task], process=Process.sequential, verbose=True)
    result = crew.kickoff()

    if not result:
        raise RuntimeError("Publish pipeline agent returned no result")
