from crewai import Crew, Process

from agents.publisher import build_publisher_agent
from agents.researcher import build_researcher_agent
from agents.writer import build_writer_agent
from agents.html_writer import build_html_writer_agent
from agents.evaluator import build_evaluator_agent

from tasks.fetch_topic_task import build_fetch_topic_task
from tasks.research_task import build_research_task
from tasks.write_task import build_write_task
from tasks.evaluate_task import build_evaluate_writing_task
from tasks.revise_writing_task import build_revise_writing_task
from tasks.html_task import build_html_task
from tasks.publish_task import build_publish_task


def build_crew(skip_research: bool = False) -> Crew:
    # Build agents
    publisher = build_publisher_agent()
    researcher = build_researcher_agent() if not skip_research else None
    writer = build_writer_agent()
    html_writer = build_html_writer_agent()
    evaluator = build_evaluator_agent()

    # Build tasks in pipeline order
    fetch_topic_task = build_fetch_topic_task(publisher)
    research_task = build_research_task(researcher, context_tasks=[fetch_topic_task]) if not skip_research else None

    write_context = [t for t in [fetch_topic_task, research_task] if t is not None]
    write_task = build_write_task(writer, context_tasks=write_context)

    # Evaluator scores the writing on three matrices (each /20, pass threshold 48/60)
    evaluate_writing_task = build_evaluate_writing_task(evaluator, context_tasks=[fetch_topic_task, write_task])

    # ConditionalTask — only runs if evaluation FAILS
    revise_writing_task = build_revise_writing_task(writer, context_tasks=[fetch_topic_task, write_task, evaluate_writing_task])

    html_task = build_html_task(html_writer, context_tasks=[fetch_topic_task, write_task, evaluate_writing_task, revise_writing_task])
    publish_task = build_publish_task(publisher, context_tasks=[fetch_topic_task, html_task, evaluate_writing_task])

    all_agents = [a for a in [publisher, researcher, writer, html_writer, evaluator] if a is not None]
    all_tasks = [t for t in [fetch_topic_task, research_task, write_task, evaluate_writing_task, revise_writing_task, html_task, publish_task] if t is not None]

    return Crew(
        agents=all_agents,
        tasks=all_tasks,
        process=Process.sequential,
        verbose=True,
    )
