def check_imports():
    from agents.evaluator import build_evaluator_agent
    from agents.html_writer import build_html_writer_agent
    from agents.manager import build_manager_agent
    from agents.publisher import build_publisher_agent
    from agents.researcher import build_researcher_agent
    from agents.writer import build_writer_agent
    from crew import build_writing_crew
    from flow import BlogFlow
    from tasks.evaluate_task import build_evaluate_writing_task
    from tasks.fetch_topic_task import build_fetch_topic_task
    from tasks.html_task import build_html_task
    from tasks.publish_task import build_publish_task
    from tasks.research_task import build_research_task
    from tasks.write_task import build_write_task
    from tools.make_webhook import parse_issue_body


def check_agent_instantiation():
    from agents.evaluator import build_evaluator_agent
    from agents.html_writer import build_html_writer_agent
    from agents.manager import build_manager_agent
    from agents.publisher import build_publisher_agent
    from agents.researcher import build_researcher_agent
    from agents.writer import build_writer_agent

    build_publisher_agent()
    build_researcher_agent()
    build_writer_agent()
    build_html_writer_agent()
    build_evaluator_agent()
    build_manager_agent()


def check_task_instantiation():
    from agents.publisher import build_publisher_agent
    from tasks.evaluate_task import build_evaluate_writing_task
    from tasks.fetch_topic_task import build_fetch_topic_task
    from tasks.html_task import build_html_task
    from tasks.publish_task import build_publish_task
    from tasks.research_task import build_research_task
    from tasks.write_task import build_write_task
    from tools.make_webhook import parse_issue_body

    publisher = build_publisher_agent()

    build_fetch_topic_task(publisher)
    parse_issue_body("", 1)
    build_research_task()
    build_write_task()
    build_evaluate_writing_task()
    build_html_task()
    build_publish_task(publisher)


def check_flow_instantiation():
    from flow import BlogFlow

    BlogFlow()
