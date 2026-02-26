from crewai.flow.flow import FlowState


class BlogFlowState(FlowState):
    topic_brief: str = ""
    html_output: str = ""
