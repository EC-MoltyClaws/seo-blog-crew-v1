from pathlib import Path
from crewai import Task

_TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "blog_post_template.html"


def build_html_task(agent, context_tasks):
    template = _TEMPLATE_PATH.read_text(encoding="utf-8")

    return Task(
        description=(
            "Convert the approved blog post draft from context into HTML using the template below. "
            "If a revised draft is present in context, use that. Otherwise use the original draft.\n\n"
            "Replace every {{PLACEHOLDER}} with the corresponding content from the draft or topic brief. "
            "Follow every RULE comment exactly — they are constraints, not suggestions. "
            "Remove all HTML comments and placeholder markers from the final output.\n\n"
            "TEMPLATE:\n\n"
            f"{template}"
        ),
        expected_output=(
            "A complete HTML document with all placeholders filled in and all comments removed, "
            "followed by the five labelled publishing fields: Title, Body, Summary, Handle, Tags."
        ),
        agent=agent,
        context=context_tasks,
    )
