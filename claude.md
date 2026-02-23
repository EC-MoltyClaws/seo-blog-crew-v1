# seo-blog-crew-v1 — Claude Instructions

## Project
CrewAI multi-agent pipeline that writes and publishes daily SEO blog posts for WanderPaws.
Agents: topic_fetcher → researcher → image_finder → writer → publisher.
Integration points: Make.com webhooks (Google Sheets + Shopify), Serper web search, Anthropic API.

Agents
- Manager
- Researcher
- Writer
- HtmlWriter
- Evaluator

Tools 
- make.com access via mcp for Manager Agent
- Some way to do research for Reasercher Agent
- Undecided tools for the evaluator agent

Different agents may use different models or even different providers


## Code Style — Simple Over Smart

**The most important rule: write code that is easy to read, not impressive to read.**

- Use plain, obvious variable names. `topic_data` not `td`. `publish_date` not `pd`.
- One thing per function. If a function does two things, split it.
- Avoid clever one-liners. A clear 3-line version is always better than a dense 1-liner.
- No unnecessary abstractions. Don't create a class when a function works fine.
- Explicit over implicit. Spell things out even if Python lets you be clever.
- Flat over nested. If you're 3 levels deep in logic, refactor.

## Error Handling

- Always handle Make.com webhook failures with a clear error message that says what failed and why.
- Never silently swallow exceptions.
- If a required env var is missing, fail immediately with a helpful message — don't let it fail later in a confusing way.

## Comments

- Write a comment when the *why* isn't obvious. Skip comments that just restate what the code does.
- Bad: `# increment counter` above `count += 1`
- Good: `# Make.com returns 200 even on logical failures, so check the response body too`

## Environment & Config

- All secrets and URLs go in `.env`. Never hardcode them.
- Use `os.getenv("VAR_NAME")` and check for None early.

## When Making Changes

- Don't refactor working code unless asked.
- When adding a feature, match the style of the existing file — don't introduce new patterns.
- If something seems overly complex, flag it and suggest a simpler version rather than just doing it.
- Prefer editing existing files over creating new ones.

## Overall Rules
- Always use Context7 MCP when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask.
- Never touch the .env file, as you risk deleting info
- All tests should be tested with a crewai Agent wherever possible to simulate realistic calling