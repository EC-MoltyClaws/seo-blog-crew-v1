from crewai import Task


def build_write_task(agent, context_tasks):
    return Task(
        description=(
            "Using the research notes provided, write a full blog post for WanderPaws. "
            "The post should be 600-900 words, have a clear intro and conclusion, "
            "and naturally include the target keyword."
        ),
        expected_output="A complete blog post in plain text, ready for HTML formatting.",
        agent=agent,
        context=context_tasks,
    )
