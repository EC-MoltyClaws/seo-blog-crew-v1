from datetime import datetime
from crewai import Task


def build_publish_task(publisher_agent):
    # Compute publish date now so the agent never has to calculate it.
    # Format: MM/DD/YYYY h:mm AM/PM (e.g. 02/26/2026 9:30 AM)
    now = datetime.now()
    hour = now.strftime("%I").lstrip("0")
    publish_date = now.strftime(f"%m/%d/%Y {hour}:%M %p")

    return Task(
        description=(
            "The blog post has been written and formatted as HTML. It is ready to publish.\n\n"
            "TOPIC BRIEF (contains blogId and metadata):\n{topic_brief}\n\n"
            "HTML OUTPUT (the formatted post ready for Shopify):\n{html_output}\n\n"
            "The HTML output ends with five labelled publishing fields: Title, Body, Summary, Handle, Tags. "
            "Use exactly those fields when calling the tool — do not use the full HTML document above them.\n\n"
            "IMPORTANT — blogBodyHtml: use only the value from the Body publishing field "
            "(the HTML content inside <body>...</body>). Do not pass the full HTML document "
            "including <html> or <head>.\n\n"
            f"Publish date and time: {publish_date}\n\n"
            "Call the Publish Blog Post to Shopify tool with:\n"
            "- blogTitle: Title field\n"
            "- blogBodyHtml: Body field\n"
            "- summaryHtml: Summary field\n"
            "- blogUrlHandle: Handle field\n"
            "- tags: Tags field\n"
            f"- blogPublishDate: {publish_date}\n"
            "- blogID: blogId from the topic brief\n"
            "- skillVersion: 'v1'"
        ),
        expected_output=(
            "Confirmation that the post was published successfully."
        ),
        agent=publisher_agent,
    )
