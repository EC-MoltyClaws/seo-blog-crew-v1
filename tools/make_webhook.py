import os
import json
import requests
from datetime import datetime
from crewai.tools import tool


@tool("Get Latest Unwritten Blog Topic")
def get_latest_topic() -> str:
    """
    Calls the Make.com 'Get Latest Unwritten Blog' webhook scenario.
    Returns the next unwritten blog topic and its associated fields from the Google Sheet as JSON.
    """
    url = os.getenv("MAKE_WEBHOOK_FETCH_TOPIC")
    api_key = os.getenv("MAKE_WEBHOOK_API_KEY")
    
    if not url:
        raise ValueError("MAKE_WEBHOOK_FETCH_TOPIC missing in .env")
    if not api_key:
        raise ValueError("MAKE_WEBHOOK_FETCH_TOPIC_API_KEY missing in .env")
    
    headers = {
    "Content-Type": "application/json",
    "x-make-apikey": api_key
}

    response = requests.post(url, json={}, headers=headers, timeout=30)

    # Make.com returns 200 even on logical failures, so check the body too
    response.raise_for_status()

    try:
        data = response.json()
    except json.JSONDecodeError as e:
        raise ValueError(f"Make.com returned non-JSON response: {e}\nBody: {response.text}")

    return json.dumps(data, indent=2)

@tool("Publish Blog Post to Shopify")
def publish_blog_post(
    blogTitle: str,
    blogBodyHtml: str,
    summaryHtml: str,
    blogUrlHandle: str,
    blogPublishDate: str,
    tags: str,
    blogID: str,
    skillVersion: str,
    imageAltText: str = None,
    imageUrl: str = None,
) -> str:
    """
    Calls the Make.com 'Post Blog To Shopify' webhook scenario to publish the blog post.
    Also updates the Google Sheet row with the post URL and publication date.

    Args:
        blogTitle: The blog post title.
        blogBodyHtml: The full HTML body of the post.
        summaryHtml: A short HTML summary/excerpt of the post.
        blogUrlHandle: The URL-friendly slug for the post.
        blogPublishDate: The publish date in MM/DD/YYYY h:mm A format (e.g. 02/23/2026 9:30 AM).
        tags: Comma-separated tags for the post.
        blogID: The Google Sheet row ID for this topic.
        skillVersion: The version identifier for the writing pipeline (e.g. 'v1').
        imageAltText: Optional. Alt text for the featured image.
        imageUrl: Optional. URL of the featured image.
    """
    url = os.getenv("MAKE_WEBHOOK_PUBLISH_POST")
    api_key = os.getenv("MAKE_WEBHOOK_API_KEY")

    if not url:
        raise ValueError("MAKE_WEBHOOK_PUBLISH_POST missing in .env")
    if not api_key:
        raise ValueError("MAKE_WEBHOOK_PUBLISH_POST_API_KEY missing in .env")

    headers = {
        "Content-Type": "application/json",
        "x-make-apikey": api_key,
    }

    # Parse and reformat the date to ensure consistent MM/DD/YYYY h:mm A output.
    # The agent may pass the hour zero-padded (e.g. "09:30 AM") — both are accepted.
    accepted_formats = ["%m/%d/%Y %I:%M %p", "%m/%d/%Y %H:%M"]
    parsed_date = None
    for fmt in accepted_formats:
        try:
            parsed_date = datetime.strptime(blogPublishDate, fmt)
            break
        except ValueError:
            continue

    if parsed_date is None:
        raise ValueError(
            f"blogPublishDate '{blogPublishDate}' is not a recognised format. "
            "Expected MM/DD/YYYY h:mm AM/PM (e.g. 02/23/2026 9:30 AM)."
        )

    hour = parsed_date.strftime("%I").lstrip("0")  # Remove leading zero from hour (e.g. "09" → "9")
    blog_publish_date = parsed_date.strftime(f"%m/%d/%Y {hour}:%M %p")

    payload = {
        "blogTitle": blogTitle,
        "blogBodyHtml": blogBodyHtml,
        "summaryHtml": summaryHtml,
        "blogUrlHandle": blogUrlHandle,
        "blogPublishDate": blog_publish_date,  # Always MM/DD/YYYY h:mm A after validation above
        "tags": tags,
        "blogID": blogID,
        "skillVersion": skillVersion,
    }

    # Only include optional image fields if provided
    if imageAltText:
        payload["imageAltText"] = imageAltText
    if imageUrl:
        payload["imageUrl"] = imageUrl

    response = requests.post(url, json=payload, headers=headers, timeout=60)

    # Make.com returns 200 even on logical failures, so check the body too
    response.raise_for_status()

    try:
        data = response.json()
    except json.JSONDecodeError as e:
        raise ValueError(f"Make.com returned non-JSON response: {e}\nBody: {response.text}")

    return json.dumps(data, indent=2)


# ── Connection test tools ─────────────────────────────────────────────────────
# Lightweight tools used only in test.py to verify each webhook is reachable.
# They do not affect production data.

@tool("Test Fetch Topic Webhook Connection")
def test_fetch_topic_connection() -> str:
    """
    Sends a test request to the fetch topic webhook and returns the raw response.
    Used to verify the Make.com connection is working before a full pipeline run.
    """
    url = os.getenv("MAKE_WEBHOOK_FETCH_TOPIC")
    api_key = os.getenv("MAKE_WEBHOOK_API_KEY")

    if not url:
        raise ValueError("MAKE_WEBHOOK_FETCH_TOPIC missing in .env")
    if not api_key:
        raise ValueError("MAKE_WEBHOOK_API_KEY missing in .env")

    headers = {
        "Content-Type": "application/json",
        "x-make-apikey": api_key,
    }

    dummy_payload = {
        "isTest": True,
    }

    response = requests.post(url, json=dummy_payload, headers=headers, timeout=30)

    # Make.com returns 200 even on logical failures, so check the body too
    response.raise_for_status()
    return f"Status: {response.status_code}\nBody: {response.text}"


@tool("Test Publish Post Webhook Connection")
def test_publish_post_connection() -> str:
    """
    Sends a dummy post to the publish webhook and returns the raw response.
    Used to verify the Make.com connection is working before a full pipeline run.
    """
    url = os.getenv("MAKE_WEBHOOK_PUBLISH_POST")
    api_key = os.getenv("MAKE_WEBHOOK_API_KEY")

    if not url:
        raise ValueError("MAKE_WEBHOOK_PUBLISH_POST missing in .env")
    if not api_key:
        raise ValueError("MAKE_WEBHOOK_API_KEY missing in .env")

    headers = {
        "Content-Type": "application/json",
        "x-make-apikey": api_key,
    }

    dummy_payload = {
        "isTest": True,
    }

    response = requests.post(url, json=dummy_payload, headers=headers, timeout=60)

    # Make.com returns 200 even on logical failures, so check the body too
    response.raise_for_status()
    return f"Status: {response.status_code}\nBody: {response.text}"