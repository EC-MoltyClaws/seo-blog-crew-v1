from crewai import Agent, Crew, Process, Task


def _run_llm_ping(llm) -> None:
    """Shared helper: spin up a single agent, ask it to reply 'ok', verify response."""
    agent = Agent(
        llm=llm,
        role="Connection Tester",
        goal="Confirm the LLM is reachable.",
        backstory="You are a connection tester. Respond only with the word: ok",
        tools=[],
        verbose=False,
    )

    task = Task(
        description="Reply with exactly the word: ok",
        expected_output="The single word: ok",
        agent=agent,
    )

    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
    result = crew.kickoff()

    if not result:
        raise RuntimeError("Agent returned an empty response")


def check_llm_flash():
    """Gemini 2.5 Flash — default LLM used by all agents except the writer."""
    from llm import get_default_llm
    _run_llm_ping(get_default_llm(verbose=False))


def check_llm_pro():
    """Gemini 2.5 Pro — higher-quality content generation."""
    from llm import get_pro_llm
    _run_llm_ping(get_pro_llm(verbose=False))
