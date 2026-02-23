"""
Tests the publisher agent's Make.com webhook connection in isolation.

Tests:
  1. test_get_latest_topic     — calls the fetch topic tool directly and prints the raw JSON response
  2. test_publish_blog_post    — runs the publisher agent through CrewAI with a dummy publish task
  3. test_fetch_topic_task     — runs the full publisher agent + fetch-topic task via CrewAI

Run with: python publisher_test.py
"""

from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Crew, Process, Task
from agents.publisher import build_publisher_agent
from tasks.fetch_topic_task import build_fetch_topic_task
from tools.make_webhook import get_latest_topic, publish_blog_post


def test_get_latest_topic():
    """Calls the Get Latest Unwritten Blog Topic tool directly, bypassing CrewAI."""
    print("\nCalling get_latest_topic tool directly...\n")

    result = get_latest_topic.run({})

    print("=" * 60)
    print("RAW TOOL RESPONSE:")
    print("=" * 60)
    print(result)


def test_publish_blog_post():
    """Runs the publisher agent through CrewAI with a dummy publish task."""
    publisher = build_publisher_agent()

    dummy_task = Task(
        description=(
            "Publish a dummy test blog post using the Publish Blog Post to Shopify tool "
            "with the following values:\n\n"
            "- blogTitle: TEST POST — Please Ignore\n"
            "- blogBodyHtml: <h1>Test Heading</h1><p>This is a dummy blog post created by the publisher test script.</p>\n"
            "- summaryHtml: <p>A dummy post used to test the Make.com publish webhook.</p>\n"
            "- blogUrlHandle: test-post-please-ignore\n"
            "- blogPublishDate: 02/23/2026 9:00 AM\n"
            "- tags: test, dummy, ignore\n"
            "- blogID: 0\n"
            "- skillVersion: v1-test\n\n"
            "Call the tool with these exact values and report back the response."
        ),
        expected_output="The raw JSON response from the Make.com publish webhook.",
        agent=publisher,
    )

    crew = Crew(
        agents=[publisher],
        tasks=[dummy_task],
        process=Process.sequential,
        verbose=True,
    )

    print("\nRunning dummy publish task via CrewAI...\n")
    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("CREW RESULT:")
    print("=" * 60)
    print(result)


def test_fetch_topic_task():
    """Runs the full publisher agent + fetch-topic task through CrewAI."""
    publisher = build_publisher_agent()
    fetch_task = build_fetch_topic_task(publisher)

    crew = Crew(
        agents=[publisher],
        tasks=[fetch_task],
        process=Process.sequential,
        verbose=True,
    )

    print("\nRunning fetch-topic task via CrewAI...\n")
    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("CREW RESULT:")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    # test_get_latest_topic()
    test_publish_blog_post()
    # test_fetch_topic_task()
