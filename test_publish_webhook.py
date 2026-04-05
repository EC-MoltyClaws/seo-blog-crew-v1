import os
import requests
from datetime import datetime
import json
import sys

def test_webhook():
    url = os.getenv("MAKE_WEBHOOK_PUBLISH_POST")
    api_key = os.getenv("MAKE_WEBHOOK_API_KEY")

    if not url or not api_key:
        print("Skipping webhook test: MAKE_WEBHOOK_PUBLISH_POST or MAKE_WEBHOOK_API_KEY missing from environment.")
        sys.exit(0) # Exit cleanly so it doesn't break CI, just skips

    headers = {
        "Content-Type": "application/json",
        "x-make-apikey": api_key,
    }

    now = datetime.now()
    hour = now.strftime("%I").lstrip("0")
    publish_date = now.strftime(f"%m/%d/%Y {hour}:%M %p")

    payload = {
        "blogTitle": "GitHub Actions Webhook Connectivity Test",
        "blogBodyHtml": "<p>This is an automated test running from GitHub Actions to verify connectivity to Make.com.</p>",
        "summaryHtml": "<p>Test payload sent from the CI pipeline.</p>",
        "blogUrlHandle": f"gh-actions-webhook-test-{now.strftime('%s')}",
        "blogPublishDate": publish_date,
        "tags": "test, github actions",
        "blogID": "test-issue-999",
        "skillVersion": "v1",
        "imageAltText": "Test image alt text",
        "imageUrl": "https://example.com/test.jpg"
    }

    print(f"Sending test payload to: {url}")
    print(json.dumps(payload, indent=2))

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        print(f"Success! Status code: {response.status_code}")
        print("Response body:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
    except Exception as e:
        print(f"Failed to post to webhook: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response body: {e.response.text}")
        sys.exit(1)

if __name__ == "__main__":
    test_webhook()
