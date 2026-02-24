from crewai import Agent, Crew, Process, Task
from llm import get_default_llm


def check_make_fetch_topic():
    """Runs a single agent with the fetch topic test tool through CrewAI."""
    from tools.make_webhook import test_fetch_topic_connection

    agent = Agent(
        llm=get_default_llm(verbose=False),
        role="Connection Tester",
        goal="Test that the fetch topic webhook is reachable.",
        backstory="You are a connection tester. You call the assigned tool and report the result.",
        tools=[test_fetch_topic_connection],
        verbose=False,
    )

    task = Task(
        description="Call the Test Fetch Topic Webhook Connection tool and report the result.",
        expected_output="The status code and raw response body from the webhook.",
        agent=agent,
    )

    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
    result = crew.kickoff()

    if not result:
        raise RuntimeError("Fetch topic agent returned no result")


def check_make_publish_post():
    """Runs a single agent with the publish post test tool through CrewAI."""
    from tools.make_webhook import test_publish_post_connection

    agent = Agent(
        llm=get_default_llm(verbose=False),
        role="Connection Tester",
        goal="Test that the publish post webhook is reachable.",
        backstory="You are a connection tester. You call the assigned tool and report the result.",
        tools=[test_publish_post_connection],
        verbose=False,
    )

    task = Task(
        description="Call the Test Publish Post Webhook Connection tool and report the result.",
        expected_output="The status code and raw response body from the webhook.",
        agent=agent,
    )

    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
    result = crew.kickoff()

    if not result:
        raise RuntimeError("Publish post agent returned no result")
