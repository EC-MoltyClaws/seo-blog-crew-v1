from crewai import Task


def build_write_task(agent, context_tasks):
    return Task(
        description=(
            "Using the topic brief and research notes from context, write a complete blog post "
            "draft for WanderPaws. The draft must include all of the following sections:\n\n"
            "1. Title — compelling and SEO-relevant\n"
            "2. Table of contents listing each major section\n"
            "3. Key takeaways: 3-5 bullet points, each under 15 words\n"
            "4. Main body: 6-8 paragraphs with clear section headers, each paragraph under 70 words\n"
            "5. Product promotion section: mention the product naturally in the flow of the content\n"
            "6. FAQ section: 5 questions with answers (3 topic-related, 2 product-related)\n"
            "7. References: full APA 7th edition entries with source URLs\n\n"
            "Also produce:\n"
            "- A concise meta description summarising the post for search engines\n"
            "- A list of relevant meta keywords for the post\n\n"
            "Write in plain, friendly English aimed at the target audience from the brief. "
            "Prioritise quality, accuracy, and engaging prose. Do not worry about HTML formatting — "
            "that is handled in a later step."
        ),
        expected_output=(
            "A complete blog post draft with all required sections: title, table of contents, "
            "key takeaways, 6-8 body paragraphs with headers, product promotion, 5-question FAQ, "
            "APA references, a meta description, and meta keywords."
        ),
        agent=agent,
        context=context_tasks,
    )
