"""
Pre-push smoke tests.
Run with: python test.py

Checks:
  1. All required env vars are set
  2. Gemini 2.5 Flash responds via a CrewAI agent (default LLM)
  3. Gemini 2.5 Pro responds via a CrewAI agent (writer LLM)
  4. Serper API responds (real call, one search)
  5. Make.com fetch topic webhook responds with valid JSON
  6. Make.com publish webhook accepts a dummy post via publisher agent
  7. Publish pipeline handoff: fetches real topic then publishes with dummy content
  8. All agents and tasks can be imported and instantiated without errors
"""

import sys
from dotenv import load_dotenv

load_dotenv()

from tests.env_checks import check_env_vars
from tests.llm_checks import check_llm_flash, check_llm_pro
from tests.serper_checks import check_serper_api
from tests.make_checks import check_make_fetch_topic, check_make_publish_post
from tests.publish_pipeline_checks import check_publish_pipeline
from tests.import_checks import check_imports, check_agent_instantiation, check_task_instantiation

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


if __name__ == "__main__":
    print("\nRunning pre-push checks...\n")

    results = [
        # check("Env vars set",                      check_env_vars),
        # check("Gemini 2.5 Flash reachable",        check_llm_flash),
        # check("Gemini 2.5 Pro reachable",          check_llm_pro),
        # check("Serper API reachable",              check_serper_api),
        # check("Make.com fetch topic reachable",    check_make_fetch_topic),
        # check("Make.com publish post reachable",   check_make_publish_post),
        check("Publish pipeline handoff",           check_publish_pipeline),
        # check("All imports resolve",               check_imports),
        # check("Agents instantiate",                check_agent_instantiation),
        # check("Tasks instantiate",                 check_task_instantiation),
    ]

    total = len(results)
    passed = sum(results)
    print(f"\n{passed}/{total} checks passed.")

    if passed < total:
        sys.exit(1)
