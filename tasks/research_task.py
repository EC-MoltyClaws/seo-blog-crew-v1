from crewai import Task


def build_research_task(agent, context_tasks):
    return Task(
        description=(
            "Read the topic brief provided in context by the manager.\n\n"
            "Using the topic, category, and target_audience from that brief, research the subject "
            "thoroughly. Find at least 2 facts or statistics that can be cited in APA format "
            "(Author, Year) and include the full source URL for each.\n\n"
            "Tailor the depth and angle of your research to the specified target audience."
        ),
        expected_output=(
            "A research summary containing:\n"
            "- The topic, category, and target audience (repeated from the brief)\n"
            "- Key facts and insights in bullet points\n"
            "- At least 2 APA-cited findings with full source URLs"
        ),
        agent=agent,
        context=context_tasks,
    )
