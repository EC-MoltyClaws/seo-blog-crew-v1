# seo-blog-crew-v1

CrewAI pipeline that researches, writes, formats, and evaluates SEO blog posts for WanderPaws.

---

## File Structure

```
seo-blog-crew-v1/
├── .env                  # API keys and webhook URLs (never committed)
├── environment.yml       # Conda environment definition
├── main.py               # Entry point — run this to kick off the crew
├── crew.py               # Assembles agents + tasks into a Crew
├── llm.py                # LLM configuration shared by all agents
├── test.py               # Pre-push smoke tests
│
├── agents/               # One file per agent
│   ├── manager.py        # Coordinates the pipeline, triggers Make.com
│   ├── researcher.py     # Searches the web for facts and sources
│   ├── writer.py         # Turns research into a blog draft
│   ├── html_writer.py    # Formats the draft as publish-ready HTML
│   └── evaluator.py      # Reviews quality, accuracy, and SEO
│
├── tasks/                # One file per task
│   ├── research_task.py  # Gather facts on a topic
│   ├── write_task.py     # Write the blog post draft
│   ├── html_task.py      # Convert draft to HTML
│   └── evaluate_task.py  # Approve or reject the post
│
└── tools/                # One file per tool
    ├── make_webhook.py   # Sends data to Make.com (used by Manager)
    └── web_search.py     # Serper web search (used by Researcher)
```

### Key conventions

- **Each agent, task, and tool lives in its own file.** To edit an agent's role or prompt, open that agent's file — nothing else needs to change.
- **`crew.py` is the only place that connects everything.** Pipeline order, which agent runs which task, and context passing are all defined there.
- **`llm.py` is the single source of truth for the model.** To switch models, change one line in `llm.py`.
- **All secrets live in `.env`.** Never hardcode keys. Never commit `.env`.

---

## Setup

```bash
conda env create -f environment.yml
conda activate seo-blog-crew-v1-env
cp .env.example .env   # then fill in your keys
```

`.env` keys required:

| Key | Purpose |
|---|---|
| `GEMINI_API_KEY` | Gemini model via LiteLLM |
| `SERPER_API_KEY` | Web search for the Researcher agent |
| `MAKE_WEBHOOK_URL` | Make.com webhook for the Manager agent |

---

## Running

```bash
python main.py
```

---

## Pre-push checks

Run before committing to catch broken imports, missing env vars, and API issues:

```bash
python test.py
```

Exits with code `1` if any check fails.

---

## Adding a new agent

1. Create `agents/your_agent.py` with a `build_your_agent()` function
2. Create `tasks/your_task.py` with a `build_your_task()` function
3. Import and wire both into `crew.py`

## Adding a new tool

1. Create `tools/your_tool.py` with a `@tool`-decorated function
2. Import it in the relevant agent file and add it to that agent's `tools=[]` list
