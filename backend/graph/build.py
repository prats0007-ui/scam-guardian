"""Assembles the LangGraph investigation graph."""
from langgraph.graph import END, START, StateGraph
import time
from .nodes import (fast_reply, judge, link_check, route_after_triage,
                    triage, web_research, write_reply)
from .state import GuardianState


def timed(name, fn):
    """Wraps a node so it prints how long it took."""
    def wrapper(state):
        start = time.perf_counter()
        result = fn(state)
        print(f"⏱ {name}: {time.perf_counter() - start:.1f}s")
        return result
    return wrapper
    
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


def investigate(message: str) -> dict:
    """Runs the full graph and returns the whole state, including the verdict."""
    return graph.invoke({"message": message})


def check_message(message: str) -> str:
    """Used by the Telegram bot: returns just the reply text."""
    return investigate(message)["reply"]
