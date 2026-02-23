from crewai import Task


def build_write_task(agent, context_tasks):
    return Task(
        description=(
            "Using the topic brief and research notes from context, write a complete blog post "
            "draft for WanderPaws. The draft must include all of the following sections:\n\n"
            "1. Title\n"
            "2. Table of contents with anchor links to each major section\n"
            "3. Key takeaways: 3-5 bullet points, each under 15 words\n"
            "4. Main body: 6-8 paragraphs, each under 70 words, "
            "with H2 headers framed as questions or direct answers\n"
            "5. Product promotion section: mention the product naturally, "
            "linking the first mention to the utm_product_url from the brief\n"
            "6. FAQ section: 5 questions (3 topic-related, 2 product-related)\n"
            "7. References: full APA 7th edition entries with source URLs\n\n"
            "Also produce:\n"
            "- A meta description of 150-160 characters\n"
            "- A URL handle in lowercase-hyphen format derived from the title\n"
            "- 8-10 comma-separated meta keywords\n\n"
            "Write in plain, friendly English aimed at the target audience from the brief."
        ),
        expected_output=(
            "A complete blog post draft with all required sections (ToC, key takeaways, "
            "6-8 body paragraphs, product promotion, 5-question FAQ, APA references) "
            "plus meta description, URL handle, and meta keywords."
        ),
        agent=agent,
        context=context_tasks,
    )
