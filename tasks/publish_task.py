from crewai import Task


def build_publish_task(publisher_agent):
    return Task(
        description=(
            "The blog post has been written and formatted as HTML. It is ready to publish.\n\n"
            "TOPIC BRIEF (contains blogId and metadata):\n{topic_brief}\n\n"
            "HTML OUTPUT (the formatted post ready for Shopify):\n{html_output}\n\n"
            "Using the five publishing fields from the HTML output "
            "(Title, Body, Summary, Handle, Tags) and the blogId from the topic brief, "
            "call the Publish Blog Post to Shopify tool to publish the post.\n\n"
            "Unless a specific date and time is provided in the topic brief, publish for current time."
        ),
        expected_output=(
            "Confirmation that the post was published successfully."
        ),
        agent=publisher_agent,
    )
