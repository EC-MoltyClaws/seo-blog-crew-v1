def check_imports():
    from agents.publisher import build_publisher_agent
    from agents.researcher import build_researcher_agent
    from agents.writer import build_writer_agent
    from agents.html_writer import build_html_writer_agent
    from agents.evaluator import build_evaluator_agent
    from tasks.fetch_topic_task import build_fetch_topic_task
    from tasks.research_task import build_research_task
    from tasks.write_task import build_write_task
    from tasks.html_task import build_html_task
    from tasks.evaluate_task import build_evaluate_writing_task
    from tasks.revise_writing_task import build_revise_writing_task
    from tasks.publish_task import build_publish_task


def check_agent_instantiation():
    from agents.publisher import build_publisher_agent
    from agents.researcher import build_researcher_agent
    from agents.writer import build_writer_agent
    from agents.html_writer import build_html_writer_agent
    from agents.evaluator import build_evaluator_agent

    build_publisher_agent()
    build_researcher_agent()
    build_writer_agent()
    build_html_writer_agent()
    build_evaluator_agent()


def check_task_instantiation():
    from agents.publisher import build_publisher_agent
    from agents.researcher import build_researcher_agent
    from agents.writer import build_writer_agent
    from agents.html_writer import build_html_writer_agent
    from agents.evaluator import build_evaluator_agent
    from tasks.fetch_topic_task import build_fetch_topic_task
    from tasks.research_task import build_research_task
    from tasks.write_task import build_write_task
    from tasks.html_task import build_html_task
    from tasks.evaluate_task import build_evaluate_writing_task
    from tasks.revise_writing_task import build_revise_writing_task
    from tasks.publish_task import build_publish_task

    publisher = build_publisher_agent()
    researcher = build_researcher_agent()
    writer = build_writer_agent()
    html_writer = build_html_writer_agent()
    evaluator = build_evaluator_agent()

    fetch_topic_task = build_fetch_topic_task(publisher)
    research_task = build_research_task(researcher, context_tasks=[fetch_topic_task])
    write_task = build_write_task(writer, context_tasks=[fetch_topic_task, research_task])
    evaluate_writing_task = build_evaluate_writing_task(evaluator, context_tasks=[fetch_topic_task, write_task])
    revise_writing_task = build_revise_writing_task(writer, context_tasks=[fetch_topic_task, write_task, evaluate_writing_task])
    html_task = build_html_task(html_writer, context_tasks=[fetch_topic_task, write_task, evaluate_writing_task, revise_writing_task])
    build_publish_task(publisher, context_tasks=[fetch_topic_task, html_task, evaluate_writing_task])
