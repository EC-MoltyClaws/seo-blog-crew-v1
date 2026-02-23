from crewai import Task


def build_html_task(agent, context_tasks):
    return Task(
        description=(
            "Convert the blog post draft into clean HTML. "
            "Use <h2> for section headings, <p> for paragraphs, and <ul>/<li> for lists. "
            "Do not add inline styles or JavaScript. Output only the HTML body content."
        ),
        expected_output="Valid HTML body content ready to paste into Shopify.",
        agent=agent,
        context=context_tasks,
    )
