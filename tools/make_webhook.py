import os
import json
import re
import requests
from datetime import datetime
from crewai.tools import tool

def get_github_headers():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN missing in .env")
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

def get_repo():
    repo = os.getenv("GITHUB_REPOSITORY")
    if not repo:
        raise ValueError("GITHUB_REPOSITORY missing in .env (e.g., 'EC-MoltyClaws/seo-blog-crew-v1')")
    return repo

@tool("Get Latest Unwritten Blog Topic")
def get_latest_topic() -> str:
    """
    Fetches the oldest open GitHub Issue with the 'blog-queue' label.
    Parses the issue body to extract topic fields.
    Returns the next unwritten blog topic and its associated fields as JSON.
    """
    headers = get_github_headers()
    repo = get_repo()
    
    url = f"https://api.github.com/repos/{repo}/issues"
    params = {
        "state": "open",
        "labels": "blog-queue",
        "sort": "created",
        "direction": "asc",
        "per_page": 1
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    issues = response.json()
    
    if not issues:
        raise ValueError("No open issues found with label 'blog-queue'.")
    
    issue = issues[0]
    body = issue.get("body", "")
    
    fields = {}
    
    def extract_field(header):
        match = re.search(rf"### {header}\s*\n+(.*?)\s*(?:\n###|\Z)", body, re.DOTALL)
        return match.group(1).strip() if match else ""

    fields["title"] = extract_field("Blog Post Title")
    fields["topic"] = extract_field("Topic")
    fields["category"] = extract_field("Category")
    fields["target_audience"] = extract_field("Target Audience")
    fields["shopify_hosted_image_link"] = extract_field("Shopify Hosted Image Link")
    fields["utm_product_url"] = extract_field("UTM Product URL")
    fields["blogId"] = str(issue["number"])
    
    # Validation
    for k, v in fields.items():
        if not v:
            print(f"Warning: Extracted empty value for '{k}' from issue #{issue['number']}")
            
    return json.dumps(fields, indent=2)

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
    Then closes the GitHub issue and logs the post to published_posts.json.
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

    hour = parsed_date.strftime("%I").lstrip("0")
    blog_publish_date = parsed_date.strftime(f"%m/%d/%Y {hour}:%M %p")

    payload = {
        "blogTitle": blogTitle,
        "blogBodyHtml": blogBodyHtml,
        "summaryHtml": summaryHtml,
        "blogUrlHandle": blogUrlHandle,
        "blogPublishDate": blog_publish_date,
        "tags": tags,
        "blogID": blogID, # Make.com will now receive Issue Number
        "skillVersion": skillVersion,
    }

    if imageAltText:
        payload["imageAltText"] = imageAltText
    if imageUrl:
        payload["imageUrl"] = imageUrl

    response = requests.post(url, json=payload, headers=headers, timeout=60)
    response.raise_for_status()

    try:
        data = response.json()
    except json.JSONDecodeError as e:
        raise ValueError(f"Make.com returned non-JSON response: {e}\nBody: {response.text}")
        
    # --- PHASE 2: Update GitHub & Log ---
    try:
        gh_headers = get_github_headers()
        repo = get_repo()
        
        # Log to JSON
        log_entry = {
            "title": blogTitle,
            "handle": blogUrlHandle,
            "publish_date": blog_publish_date,
            "issue_number": blogID,
            "shopify_tags": tags
        }
        
        log_file = "published_posts.json"
        log_data = []
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                try:
                    log_data = json.load(f)
                except:
                    pass
        log_data.append(log_entry)
        with open(log_file, "w") as f:
            json.dump(log_data, f, indent=2)

        # Comment and close Issue
        issue_number = blogID
        comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
        requests.post(comment_url, headers=gh_headers, json={"body": f"🎉 **Published successfully!**\n\n**Title:** {blogTitle}\n**Date:** {blog_publish_date}"}).raise_for_status()
        
        issue_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
        requests.patch(issue_url, headers=gh_headers, json={"state": "closed", "state_reason": "completed"}).raise_for_status()
        
    except Exception as e:
        print(f"Warning: Make.com succeeded, but GitHub/JSON update failed: {e}")

    return json.dumps(data, indent=2)

@tool("Get Published Shopify Blog Posts")
def get_shopify_blog_posts() -> str:
    url = os.getenv("MAKE_WEBHOOK_FETCH_BLOG_POSTS")
    api_key = os.getenv("MAKE_WEBHOOK_API_KEY")

    if not url:
        raise ValueError("MAKE_WEBHOOK_FETCH_BLOG_POSTS missing in .env")
    if not api_key:
        raise ValueError("MAKE_WEBHOOK_API_KEY missing in .env")

    headers = {
        "Content-Type": "application/json",
        "x-make-apikey": api_key,
    }

    response = requests.post(url, json={}, headers=headers, timeout=30)
    response.raise_for_status()

    try:
        data = response.json()
    except json.JSONDecodeError as e:
        raise ValueError(f"Make.com returned non-JSON response: {e}\nBody: {response.text}")

    return json.dumps(data, indent=2)

@tool("Test Fetch Topic Webhook Connection")
def test_fetch_topic_connection() -> str:
    return "Skipped. Now using GitHub API."

@tool("Test Shopify Blog Posts Webhook Connection")
def test_shopify_blog_posts_connection() -> str:
    url = os.getenv("MAKE_WEBHOOK_FETCH_BLOG_POSTS")
    api_key = os.getenv("MAKE_WEBHOOK_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "x-make-apikey": api_key,
    }
    response = requests.post(url, json={"isTest": True}, headers=headers, timeout=30)
    response.raise_for_status()
    return f"Status: {response.status_code}\nBody: {response.text}"

@tool("Test Publish Post Webhook Connection")
def test_publish_post_connection() -> str:
    url = os.getenv("MAKE_WEBHOOK_PUBLISH_POST")
    api_key = os.getenv("MAKE_WEBHOOK_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "x-make-apikey": api_key,
    }
    response = requests.post(url, json={"isTest": True}, headers=headers, timeout=60)
    response.raise_for_status()
    return f"Status: {response.status_code}\nBody: {response.text}"
