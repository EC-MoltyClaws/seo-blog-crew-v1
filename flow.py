from crewai import Crew, Process
from crewai.flow import Flow, listen, start

from agents.publisher import build_publisher_agent
from crew import build_writing_crew
from state import BlogFlowState
from tasks.fetch_topic_task import build_fetch_topic_task
from tasks.publish_task import build_publish_task


class BlogFlow(Flow[BlogFlowState]):
    def __init__(self):
        super().__init__()
        publisher = build_publisher_agent()
        self._fetch_crew = Crew(
            agents=[publisher],
            tasks=[build_fetch_topic_task(publisher)],
            process=Process.sequential,
            verbose=True,
        )
        self._writing_crew = build_writing_crew()
        self._publish_crew = Crew(
            agents=[publisher],
            tasks=[build_publish_task(publisher)],
            process=Process.sequential,
            verbose=True,
        )

    @start()
    def fetch_topic(self):
        result = self._fetch_crew.kickoff()
        self.state.topic_brief = result.raw

    @listen("fetch_topic")
    def write_blog(self):
        result = self._writing_crew.kickoff(inputs={"topic_brief": self.state.topic_brief})
        self.state.html_output = result.raw

    @listen("write_blog")
    def publish(self):
        self._publish_crew.kickoff(inputs={
            "topic_brief": self.state.topic_brief,
            "html_output": self.state.html_output,
        })
