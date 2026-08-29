from langgraph.graph import StateGraph, START, END

from app.graph.state import ReviewState
from app.agents.bug_agent import bug_agent
from app.agents.security_agent import security_agent
from app.agents.quality_agent import quality_agent


def build_review_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("bug_agent", bug_agent)
    graph.add_node("security_agent", security_agent)
    graph.add_node("quality_agent", quality_agent)

    graph.add_edge(START, "bug_agent")
    graph.add_edge(START, "security_agent")
    graph.add_edge(START, "quality_agent")

    graph.add_edge("bug_agent", END)
    graph.add_edge("security_agent", END)
    graph.add_edge("quality_agent", END)

    return graph.compile()