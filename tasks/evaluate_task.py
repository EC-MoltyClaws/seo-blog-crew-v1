from crewai import Task


def build_evaluate_task(agent, context_tasks):
    return Task(
        description=(
            "Review the blog post for quality, factual accuracy, and SEO. "
            "Check that it reads naturally, targets the keyword correctly, "
            "and meets WanderPaws content standards. "
            "Return APPROVED or REJECTED with a short reason."
        ),
        expected_output="APPROVED or REJECTED with a one-paragraph explanation.",
        agent=agent,
        context=context_tasks,
    )
