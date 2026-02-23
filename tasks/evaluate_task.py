from crewai import Task


def build_evaluate_task(agent, context_tasks):
    return Task(
        description=(
            "Review the HTML blog post and publishing fields from context against "
            "the WanderPaws publishing checklist. Check every item below:\n\n"
            "[ ] At least 2 APA in-text citations present in the body\n"
            "[ ] References section has full APA 7th edition entries with URLs\n"
            "[ ] FAQ contains exactly 5 questions (3 topic-related, 2 product-related)\n"
            "[ ] Product promotion block uses data-slate markup with a 383x383 image\n"
            "[ ] First product mention links to the UTM URL\n"
            "[ ] Summary (meta description) is between 150 and 160 characters\n"
            "[ ] Handle is lowercase letters and hyphens only\n"
            "[ ] Tags is a non-empty comma-separated keyword string\n"
            "[ ] HTML is well-formed with no unclosed tags\n\n"
            "Return APPROVED if all checks pass. "
            "Return REJECTED followed by a numbered list of every failed check if any item fails."
        ),
        expected_output=(
            "APPROVED, or REJECTED with a numbered list of every failed checklist item."
        ),
        agent=agent,
        context=context_tasks,
    )
