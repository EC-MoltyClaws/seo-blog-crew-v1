"""
Pre-push smoke tests.
Run with: python test.py

Checks:
  1. All required env vars are set
  2. Gemini API responds (real call, tiny prompt)
  3. Serper API responds (real call, one search)
  4. Make.com fetch topic webhook responds with valid JSON
  5. Make.com publish webhook accepts a dummy post via publisher agent
  6. All agents and tasks can be imported and instantiated without errors
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

PASS = "  PASS"
FAIL = "  FAIL"


def check(label: str, fn):
    try:
        fn()
        print(f"{PASS}  {label}")
        return True
    except Exception as e:
        print(f"{FAIL}  {label}")
        print(f"        {e}")
        return False


# ── 1. Env vars ──────────────────────────────────────────────────────────────

def check_env_vars():
    required = [
        "GEMINI_API_KEY",
        "SERPER_API_KEY",
        "MAKE_WEBHOOK_FETCH_TOPIC",
        "MAKE_WEBHOOK_API_KEY",
        "MAKE_WEBHOOK_PUBLISH_POST",
    ]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        raise ValueError(f"Missing env vars: {', '.join(missing)}")


# ── 2. Gemini API ─────────────────────────────────────────────────────────────

def check_gemini_api():
    from llm import get_default_llm

    llm = get_default_llm(verbose=False)
    response = llm.call(messages=[{"role": "user", "content": "Reply with just the word: ok"}])
    if not response:
        raise RuntimeError("Empty response from Gemini API")


# ── 3. Serper API ─────────────────────────────────────────────────────────────

def check_serper_api():
    import requests

    response = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": os.getenv("SERPER_API_KEY"), "Content-Type": "application/json"},
        json={"q": "wanderpaws pet travel", "num": 1},
        timeout=10,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Serper returned {response.status_code}: {response.text}")
    if not response.json().get("organic"):
        raise RuntimeError("Serper returned no results")


# ── 4. Make.com webhooks ───────────────────────────────────────────────────────
# Each check runs a single agent with the test tool via CrewAI so the call path
# mirrors production as closely as possible (same LLM, same tool-calling mechanism).

def check_make_fetch_topic():
    """Runs a single agent with the fetch topic test tool through CrewAI."""
    from crewai import Agent, Crew, Process, Task
    from llm import get_default_llm
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
    from crewai import Agent, Crew, Process, Task
    from llm import get_default_llm
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


# ── 5. Imports and instantiation ──────────────────────────────────────────────

def check_imports():
    from agents.manager import build_manager_agent
    from agents.publisher import build_publisher_agent
    from agents.researcher import build_researcher_agent
    from agents.writer import build_writer_agent
    from agents.html_writer import build_html_writer_agent
    from agents.evaluator import build_evaluator_agent
    from tasks.fetch_topic_task import build_fetch_topic_task
    from tasks.research_task import build_research_task
    from tasks.write_task import build_write_task
    from tasks.html_task import build_html_task
    from tasks.evaluate_task import build_evaluate_task
    from tasks.publish_task import build_publish_task


def check_agent_instantiation():
    from agents.manager import build_manager_agent
    from agents.publisher import build_publisher_agent
    from agents.researcher import build_researcher_agent
    from agents.writer import build_writer_agent
    from agents.html_writer import build_html_writer_agent
    from agents.evaluator import build_evaluator_agent

    build_manager_agent()
    build_publisher_agent()
    build_researcher_agent()
    build_writer_agent()
    build_html_writer_agent()
    build_evaluator_agent()


def check_task_instantiation():
    from agents.publisher import build_publisher_agent
    from agents.researcher import build_researcher_agent
    from agents.writer import build_writer_agent
    from agents.html_writer import build_html_writer_agent
    from agents.evaluator import build_evaluator_agent
    from tasks.fetch_topic_task import build_fetch_topic_task
    from tasks.research_task import build_research_task
    from tasks.write_task import build_write_task
    from tasks.html_task import build_html_task
    from tasks.evaluate_task import build_evaluate_task
    from tasks.publish_task import build_publish_task

    publisher = build_publisher_agent()
    researcher = build_researcher_agent()
    writer = build_writer_agent()
    html_writer = build_html_writer_agent()
    evaluator = build_evaluator_agent()

    fetch_topic_task = build_fetch_topic_task(publisher)
    research_task = build_research_task(researcher, context_tasks=[fetch_topic_task])
    write_task = build_write_task(writer, context_tasks=[fetch_topic_task, research_task])
    html_task = build_html_task(html_writer, context_tasks=[fetch_topic_task, write_task])
    evaluate_task = build_evaluate_task(evaluator, context_tasks=[write_task, html_task])
    build_publish_task(publisher, context_tasks=[fetch_topic_task, html_task, evaluate_task])


# ── Run all checks ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\nRunning pre-push checks...\n")

    results = [
        check("Env vars set",                      check_env_vars),
        # check("Gemini API reachable",             check_gemini_api),
        # check("Serper API reachable",             check_serper_api),
        check("Make.com fetch topic reachable",    check_make_fetch_topic),
        check("Make.com publish post reachable",   check_make_publish_post),
        # check("All imports resolve",              check_imports),
        # check("Agents instantiate",               check_agent_instantiation),
        # check("Tasks instantiate",                check_task_instantiation),
    ]

    total = len(results)
    passed = sum(results)
    print(f"\n{passed}/{total} checks passed.")

    if passed < total:
        sys.exit(1)
