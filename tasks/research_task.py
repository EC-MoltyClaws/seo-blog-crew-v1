from crewai import Task


def build_research_task():
    return Task(
        description=(
            "Research the following blog topic thoroughly.\n\n"
            "TOPIC BRIEF:\n{topic_brief}\n\n"
            "Using the topic, category, and target_audience from the brief above, find at least "
            "2 facts or statistics that can be cited in APA format (Author, Year) and include "
            "the full source URL for each.\n\n"
            "Tailor the depth and angle of your research to the target_audience specified in the brief.\n\n"
            "Also call the Get Published Shopify Blog Posts tool to retrieve the list of existing "
            "WanderPaws blog posts. From that list, identify up to 3 posts that are relevant to "
            "this topic and include their exact titles and URLs in your output under "
            "'Related WanderPaws Posts'. The writer will use these for internal linking — "
            "do not invent or guess any blog post URLs."
        ),
        expected_output=(
            "A research summary containing:\n"
            "- The topic, category, and target audience (repeated from the brief)\n"
            "- Key facts and insights in bullet points\n"
            "- At least 2 APA-cited findings with full source URLs\n"
            "- Related WanderPaws Posts: up to 3 existing post titles and their exact URLs "
            "(from the Shopify blog posts tool), or a note that no relevant posts were found"
        ),
    )
