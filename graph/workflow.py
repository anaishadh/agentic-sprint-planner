from langgraph.graph import StateGraph, END
from core.state import SprintState
from agents.business_analyst import business_analyst_agent
from agents.task_breakdown import task_breakdown_agent
from agents.allocator import allocate_tasks
from agents.scheduler import schedule_tasks

def build_graph():
    graph = StateGraph(SprintState)

    graph.add_node("business_analyst", business_analyst_agent)
    graph.add_node("task_breakdown", task_breakdown_agent)
    graph.add_node("task_allocator", allocate_tasks)
    graph.add_node("scheduler", schedule_tasks)

    graph.set_entry_point("business_analyst")
    graph.add_edge("business_analyst", "task_breakdown")
    graph.add_edge("task_breakdown", "task_allocator")
    graph.add_edge("task_allocator", "scheduler")
    graph.add_edge("scheduler", END)

    return graph.compile()
