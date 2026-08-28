from langgraph.graph import StateGraph,START,END

from app.graph.state  import ReviewState
from app.agents.bug_agent import bug_agent


def build_review_graph():
    graph=StateGraph(ReviewState)


    graph.add_node(
        "bug_agent",
        bug_agent
    )

    graph.add_edge(
        START,
        "bug_agent",
    )

    graph.add_edge(
        "bug_agent",
        END
    )

    return graph.compile()