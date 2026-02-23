from crewai import Task


def build_html_task(agent, context_tasks):
    return Task(
        description=(
            "Convert the blog post draft from context into a complete HTML document "
            "matching the WanderPaws Shopify blog template.\n\n"
            "Requirements:\n"
            "- Use <h1> for the post title, <h2> for main sections, <h3> for FAQ entries\n"
            "- Wrap the product promotion image in the correct data-slate markup at 383x383 px, "
            "using the shopify_image_url from the manager's brief\n"
            "- Link the first product mention to the utm_product_url from the brief\n"
            "- Preserve all APA citations and the references section\n\n"
            "Then output the five publishing fields the manager needs for Make.com:\n"
            "- Title: plain text from the <title> tag\n"
            "- Body: the full <body> HTML string\n"
            "- Summary: the meta description (150-160 chars)\n"
            "- Handle: lowercase-hyphen URL handle\n"
            "- Tags: comma-separated meta keywords string"
        ),
        expected_output=(
            "A valid HTML document followed by the five labelled publishing fields: "
            "Title, Body, Summary, Handle, Tags."
        ),
        agent=agent,
        context=context_tasks,
    )
