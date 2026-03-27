from crewai import Task


def build_fetch_topic_task(publisher_agent):
    return Task(
        description=(
            "Call the 'Get Latest Unwritten Blog Topic' tool to retrieve "
            "the next blog topic from the GitHub Issues queue.\n\n"
            "From the response, extract and return all of the following fields:\n"
            "- title: the exact blog post title as provided in the issue — this must not be changed by any agent\n"
            "- topic: the blog post subject\n"
            "- category: the content category\n"
            "- target_audience: who the post is written for\n"
            "- shopify_hosted_image_link: the 383x383 product image URL from the issue\n"
            "- utm_product_url: the UTM-tagged product link\n"
            "- blogId: the unique GitHub Issue number for this blog entry (needed to close it later)\n\n"
            "Return these as a clearly labelled brief so every downstream agent knows exactly "
            "what topic to research and write about."
        ),
        expected_output=(
            "A structured topic brief with these labelled fields: "
            "title, topic, category, target_audience, shopify_hosted_image_link, utm_product_url, blogId."
        ),
        agent=publisher_agent,
    )
