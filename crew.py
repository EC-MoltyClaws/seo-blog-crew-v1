from crewai import Crew, Process

from agents.manager import build_manager_agent
from agents.publisher import build_publisher_agent
from agents.researcher import build_researcher_agent
from agents.writer import build_writer_agent
from agents.html_writer import build_html_writer_agent
from agents.evaluator import build_evaluator_agent

from tasks.fetch_topic_task import build_fetch_topic_task
from tasks.research_task import build_research_task
from tasks.write_task import build_write_task
from tasks.html_task import build_html_task
from tasks.evaluate_task import build_evaluate_task
from tasks.publish_task import build_publish_task


def build_crew() -> Crew:
    # Build agents
    manager = build_manager_agent()
    publisher = build_publisher_agent()
    researcher = build_researcher_agent()
    writer = build_writer_agent()
    html_writer = build_html_writer_agent()
    evaluator = build_evaluator_agent()

    # Build tasks in pipeline order
    fetch_topic_task = build_fetch_topic_task(publisher)
    research_task = build_research_task(researcher, context_tasks=[fetch_topic_task])
    write_task = build_write_task(writer, context_tasks=[fetch_topic_task, research_task])
    html_task = build_html_task(html_writer, context_tasks=[fetch_topic_task, write_task])
    evaluate_task = build_evaluate_task(evaluator, context_tasks=[write_task, html_task])
    publish_task = build_publish_task(publisher, context_tasks=[fetch_topic_task, html_task, evaluate_task])

    return Crew(
        agents=[publisher, researcher, writer, html_writer, evaluator],
        tasks=[fetch_topic_task, research_task, write_task, html_task, evaluate_task, publish_task],
        manager_agent=manager,
        process=Process.hierarchical,
        verbose=True,
    )
