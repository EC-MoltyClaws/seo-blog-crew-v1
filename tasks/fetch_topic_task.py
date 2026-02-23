from crewai import Task


def build_fetch_topic_task(publisher_agent):
    return Task(
        description=(
            "Call the Make.com 'Get Latest Unwritten Blog' scenario to retrieve "
            "the next blog topic that has a blank post date in the Main Google Sheet.\n\n"
            "From the response, extract and return all of the following fields:\n"
            "- topic: the blog post subject\n"
            "- category: the content category\n"
            "- target_audience: who the post is written for\n"
            "- shopify_image_url: the 383x383 product image URL from the sheet\n"
            "- utm_product_url: the UTM-tagged product link\n"
            "- row_number: the sheet row this topic came from (needed to update it later)\n\n"
            "Return these as a clearly labelled brief so every downstream agent knows exactly "
            "what topic to research and write about."
        ),
        expected_output=(
            "A structured topic brief with these labelled fields: "
            "topic, category, target_audience, shopify_image_url, utm_product_url, row_number."
        ),
        agent=publisher_agent,
    )
