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
    required = ["GEMINI_API_KEY", "SERPER_API_KEY", "MAKE_MCP_URL", "MAKE_MCP_TOKEN"]
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
    from crewai.mcp import MCPServerSSE
    from tools.make_webhook import get_make_mcp_server

    server = get_make_mcp_server()

    if not isinstance(server, MCPServerSSE):
        raise TypeError(f"Expected MCPServerSSE, got {type(server)}")

    expected_url = os.getenv("MAKE_MCP_URL")
    if server.url != expected_url:
        raise ValueError(f"Server URL mismatch: expected {expected_url}, got {server.url}")

    auth_header = server.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise ValueError("Authorization header is missing or malformed")


def check_make_mcp_reachable():
    from crewai_tools import MCPServerAdapter
    from tools.make_webhook import get_make_mcp_server

    server = get_make_mcp_server()

    # MCPServerAdapter is the same layer CrewAI uses internally when an agent runs.
    # MCPServerSSE is config-only — it has no standalone connect/list_tools API.
    server_params = {"url": f"{server.url}/sse", "headers": server.headers, "transport": "sse"}

    with MCPServerAdapter(server_params) as tools:
        if not isinstance(tools, list):
            raise RuntimeError("MCPServerAdapter did not return a tools list")
        print(f"\n        Found {len(tools)} tool(s): {[t.name for t in tools]}")


# ── 5. Imports and instantiation ──────────────────────────────────────────────

def check_imports():
    from agents.manager import build_manager_agent
    from agents.researcher import build_researcher_agent
    from agents.writer import build_writer_agent
    from agents.html_writer import build_html_writer_agent
    from agents.evaluator import build_evaluator_agent
    from tasks.research_task import build_research_task
    from tasks.write_task import build_write_task
    from tasks.html_task import build_html_task
    from tasks.evaluate_task import build_evaluate_task


def check_agent_instantiation():
    from agents.manager import build_manager_agent
    from agents.researcher import build_researcher_agent
    from agents.writer import build_writer_agent
    from agents.html_writer import build_html_writer_agent
    from agents.evaluator import build_evaluator_agent

    build_manager_agent()
    build_researcher_agent()
    build_writer_agent()
    build_html_writer_agent()
    build_evaluator_agent()


def check_task_instantiation():
    from agents.researcher import build_researcher_agent
    from agents.writer import build_writer_agent
    from agents.html_writer import build_html_writer_agent
    from agents.evaluator import build_evaluator_agent
    from tasks.research_task import build_research_task
    from tasks.write_task import build_write_task
    from tasks.html_task import build_html_task
    from tasks.evaluate_task import build_evaluate_task

    researcher = build_researcher_agent()
    writer = build_writer_agent()
    html_writer = build_html_writer_agent()
    evaluator = build_evaluator_agent()

    research_task = build_research_task(researcher, "test topic")
    write_task = build_write_task(writer, context_tasks=[research_task])
    html_task = build_html_task(html_writer, context_tasks=[write_task])
    build_evaluate_task(evaluator, context_tasks=[write_task, html_task])


# ── Run all checks ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\nRunning pre-push checks...\n")

    results = [
        check("Env vars set",              check_env_vars),
        check("Gemini API reachable",      check_gemini_api),
        check("Serper API reachable",      check_serper_api),
        check("Make MCP config valid",     check_make_mcp_config),
        check("Make MCP lists tools",      check_make_mcp_reachable),
        check("All imports resolve",       check_imports),
        check("Agents instantiate",        check_agent_instantiation),
        check("Tasks instantiate",         check_task_instantiation),
    ]

    total = len(results)
    passed = sum(results)
    print(f"\n{passed}/{total} checks passed.")

    if passed < total:
        sys.exit(1)
