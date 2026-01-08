from langgraph.graph import StateGraph, END
from core.state import SprintState
from agents.business_analyst import business_analyst_agent


def build_graph():
    graph = StateGraph(SprintState)

    graph.add_node("business_analyst", business_analyst_agent)

    graph.set_entry_point("business_analyst")
    graph.add_edge("business_analyst", END)

    return graph.compile()
