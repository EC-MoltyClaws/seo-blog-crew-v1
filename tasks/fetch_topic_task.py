from crewai import Task


def build_fetch_topic_task(publisher_agent):
    return Task(
        description=(
            "Call the Make.com 'Get Latest Unwritten Blog' scenario to retrieve "
            "the next blog topic that has a blank post date in the Main Google Sheet.\n\n"
            "From the response, extract and return all of the following fields:\n"
            "- title: the exact blog post title as provided in the sheet — this must not be changed by any agent\n"
            "- topic: the blog post subject\n"
            "- category: the content category\n"
            "- target_audience: who the post is written for\n"
            "- shopify_hosted_image_link: the 383x383 product image URL from the sheet\n"
            "- utm_product_url: the UTM-tagged product link\n"
            "- blogId: the unique identifier for this blog entry (needed to update it later)\n\n"
            "Return these as a clearly labelled brief so every downstream agent knows exactly "
            "what topic to research and write about."
        ),
        expected_output=(
            "A structured topic brief with these labelled fields: "
            "title, topic, category, target_audience, shopify_hosted_image_link, utm_product_url, blogId."
        ),
        agent=publisher_agent,
    )
