import os


def check_env_vars():
    required = [
        "GEMINI_API_KEY",
        "SERPER_API_KEY",
        "MAKE_WEBHOOK_FETCH_TOPIC",
        "MAKE_WEBHOOK_API_KEY",
        "MAKE_WEBHOOK_PUBLISH_POST",
        "MAKE_WEBHOOK_FETCH_BLOG_POSTS",
    ]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        raise ValueError(f"Missing env vars: {', '.join(missing)}")
