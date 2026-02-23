"""
Pre-push smoke tests.
Run with: python test.py

Checks:
  1. All required env vars are set
  2. Gemini API responds (real call, tiny prompt)
  3. Serper API responds (real call, one search)
  4. Make.com MCP server config is valid and endpoint is reachable
  5. All agents and tasks can be imported and instantiated without errors
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
    required = ["GEMINI_API_KEY", "SERPER_API_KEY", "MAKE_MCP_TOKEN"]
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


# ── 4. Make.com MCP ───────────────────────────────────────────────────────────

def check_make_mcp_config():
    # from tools.make_webhook import get_mcp_url

    # toolBoxUrl = os.getenv("MAKE_MCP_TOOLBOX_URL")
    # toolBoxKey = os.getenv("MAKE_MCP_TOOLBOX_KEY")


    # if not url.endswith("/sse"):
    #     raise ValueError(f"MCP URL must end with /sse, got: {url}")


def check_make_mcp_reachable():
    from crewai import Agent
    from tools.make_webhook import get_mcp_sse
    from llm import get_default_llm

    # Mirror the exact DSL used in publisher.py — mcps=[url_string]
    # If CrewAI can load tools from the URL the agent will have a non-empty tools list
    agent = Agent(
        llm=get_default_llm(verbose=False),
        role="Test",
        goal="Test",
        backstory="Test",
        mcps=[get_mcp_sse()],
    )
    if not agent.tools:
        raise RuntimeError("DSL MCP loaded no tools onto the agent")


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
        # check("Env vars set",              check_env_vars),
        # check("Gemini API reachable",      check_gemini_api),
        # check("Serper API reachable",      check_serper_api),
        check("Make MCP config valid",     check_make_mcp_config),
        check("Make MCP lists tools",      check_make_mcp_reachable),
        # check("All imports resolve",       check_imports),
        # check("Agents instantiate",        check_agent_instantiation),
        # check("Tasks instantiate",         check_task_instantiation),
    ]

    total = len(results)
    passed = sum(results)
    print(f"\n{passed}/{total} checks passed.")

    if passed < total:
        sys.exit(1)
