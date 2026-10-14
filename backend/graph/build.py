"""Assembles the LangGraph investigation graph."""
from langgraph.graph import END, START, StateGraph

from .nodes import (fast_reply, judge, link_check, route_after_triage,
                    triage, web_research, write_reply)
from .state import GuardianState


def build_graph():
    g = StateGraph(GuardianState)
    g.add_node("triage", triage)
    g.add_node("link_check", link_check)
    g.add_node("web_research", web_research)
    g.add_node("judge", judge)
    g.add_node("fast_reply", fast_reply)
    g.add_node("write_reply", write_reply)

    g.add_edge(START, "triage")
    g.add_conditional_edges("triage", route_after_triage,
                            ["link_check", "web_research", "fast_reply"])
    g.add_edge(["link_check", "web_research"], "judge")  # waits for both
    g.add_edge("judge", "write_reply")
    g.add_edge("fast_reply", "write_reply")
    g.add_edge("write_reply", END)
    return g.compile()


graph = build_graph()


def check_message(message: str) -> str:
    result = graph.invoke({"message": message})
    return result["reply"]
