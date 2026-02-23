from crewai import Crew, Process

from agents.manager import build_manager_agent
from agents.researcher import build_researcher_agent
from agents.writer import build_writer_agent
from agents.html_writer import build_html_writer_agent
from agents.evaluator import build_evaluator_agent

from tasks.research_task import build_research_task
from tasks.write_task import build_write_task
from tasks.html_task import build_html_task
from tasks.evaluate_task import build_evaluate_task


def build_crew(topic: str) -> Crew:
    # Build agents
    manager = build_manager_agent()
    researcher = build_researcher_agent()
    writer = build_writer_agent()
    html_writer = build_html_writer_agent()
    evaluator = build_evaluator_agent()

    # Build tasks in pipeline order
    research_task = build_research_task(researcher, topic)
    write_task = build_write_task(writer, context_tasks=[research_task])
    html_task = build_html_task(html_writer, context_tasks=[write_task])
    evaluate_task = build_evaluate_task(evaluator, context_tasks=[write_task, html_task])

    return Crew(
        agents=[researcher, writer, html_writer, evaluator],
        tasks=[research_task, write_task, html_task, evaluate_task],
        manager_agent=manager,
        process=Process.hierarchical,
        verbose=True,
    )
