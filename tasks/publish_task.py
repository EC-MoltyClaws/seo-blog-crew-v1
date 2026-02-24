from crewai import Task


def build_publish_task(publisher_agent, context_tasks):
    return Task(
        description=(
            "The blog post has been evaluated. If the evaluation result is APPROVED, proceed.\n\n"
            "Using the five publishing fields from the HTML formatter's output "
            "(Title, Body, Summary, Handle, Tags) and the blogId from the topic brief:\n\n"
            "1. Call the Make.com 'Post Blog To Shopify' scenario with the "
            "Title, Body, Summary, Handle, and Tags fields to publish the post.\n\n"
            "2. From the publish response, extract the post URL and short URL.\n\n"
            "3. Update the Main Google Sheet row (using blogId) with:\n"
            "   - Written By: 'v1'\n"
            "   - Post Date: today's date in MM/DD/YYYY format\n"
            "   - Post URL: the full post URL from the publish response\n"
            "   - Short URL: the short URL from the publish response\n\n"
            "If the evaluation result is REJECTED, do not publish. "
            "Report the rejection reason instead."
        ),
        expected_output=(
            "Confirmation that the post was published with the post URL, "
            "or a clear rejection report if the evaluation did not pass."
        ),
        agent=publisher_agent,
        context=context_tasks,
    )
