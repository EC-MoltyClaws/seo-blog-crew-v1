from crewai import Crew, Process

from agents.evaluator import build_evaluator_agent
from agents.html_writer import build_html_writer_agent
from agents.manager import build_manager_agent
from agents.researcher import build_researcher_agent
from agents.writer import build_writer_agent
from tasks.evaluate_task import build_evaluate_writing_task
from tasks.html_task import build_html_task
from tasks.research_task import build_research_task
from tasks.write_task import build_write_task


def build_writing_crew() -> Crew:
    manager = build_manager_agent()
    researcher = build_researcher_agent()
    writer = build_writer_agent()
    html_writer = build_html_writer_agent()
    evaluator = build_evaluator_agent()

    return Crew(
        agents=[researcher, writer, html_writer, evaluator],
        tasks=[
            build_research_task(),
            build_write_task(),
            build_evaluate_writing_task(),
            build_html_task(),
        ],
        process=Process.hierarchical,
        manager_agent=manager,
        verbose=True,
    )
