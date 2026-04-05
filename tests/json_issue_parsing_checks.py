import sys
import types


if "crewai" not in sys.modules:
    crewai_module = types.ModuleType("crewai")
    tools_module = types.ModuleType("crewai.tools")

    def tool(name=None):
        def decorator(fn):
            return fn

        return decorator

    tools_module.tool = tool
    crewai_module.tools = tools_module
    sys.modules["crewai"] = crewai_module
    sys.modules["crewai.tools"] = tools_module

from tools.make_webhook import parse_issue_body


LEGACY_BODY = """
### Blog Post Title

The Cat Backpack Buyers Guide

### Topic

How to choose the right cat backpack.

### Category

Product Guide

### Target Audience

Cat parents shopping for travel gear.

### Shopify Hosted Image Link

https://example.com/image.jpg

### UTM Product URL

https://getwanderpaws.com/products/cat-backpack?utm_source=github
"""

JSON_BODY = """
### JSON Payload

```json
{
  "title": "Cat Backpack Buying Guide",
  "topic": "How to choose the right cat backpack",
  "category": "Product Guide",
  "target_audience": "Cat parents who travel",
  "shopify_hosted_image_link": "https://example.com/image.jpg",
  "utm_product_url": "https://getwanderpaws.com/products/cat-backpack?utm_source=github",
  "blogId": ""
}
```
"""


def check_json_issue_parsing():
    parsed = parse_issue_body(JSON_BODY, 42)

    assert parsed == {
        "title": "Cat Backpack Buying Guide",
        "topic": "How to choose the right cat backpack",
        "category": "Product Guide",
        "target_audience": "Cat parents who travel",
        "shopify_hosted_image_link": "https://example.com/image.jpg",
        "utm_product_url": "https://getwanderpaws.com/products/cat-backpack?utm_source=github",
        "blogId": "42",
    }


def check_legacy_issue_parsing():
    parsed = parse_issue_body(LEGACY_BODY, 1)

    assert parsed == {
        "title": "The Cat Backpack Buyers Guide",
        "topic": "How to choose the right cat backpack.",
        "category": "Product Guide",
        "target_audience": "Cat parents shopping for travel gear.",
        "shopify_hosted_image_link": "https://example.com/image.jpg",
        "utm_product_url": "https://getwanderpaws.com/products/cat-backpack?utm_source=github",
        "blogId": "1",
    }
