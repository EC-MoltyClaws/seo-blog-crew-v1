from crewai import Task


def build_research_task(agent, topic):
    return Task(
        description=(
            f"Research the following topic for a WanderPaws blog post: {topic}\n\n"
            "Find key facts, useful tips, and any relevant statistics. "
            "Summarise your findings in clear bullet points."
        ),
        expected_output="A bullet-point summary of research findings ready for the writer.",
        agent=agent,
    )
