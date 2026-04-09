from langgraph.graph import StateGraph, END
from ..graph.state import AgentState
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.triage_agent import triage_agent
from agents.rag_agent import rag_agent
from agents.planner_agent import planner_agent
from agents.interactive_nodes import ask_info_node, feedback_node

def create_workflow():
    """Create the LangGraph workflow with interactive diagnostic loop."""

    workflow = StateGraph(AgentState)

    # Add all nodes
    workflow.add_node("triage", triage_agent)
    workflow.add_node("rag", rag_agent)
    workflow.add_node("planner", planner_agent)
    workflow.add_node("ask_info", ask_info_node)
    workflow.add_node("feedback", feedback_node)

    # Set entry point
    workflow.set_entry_point("triage")

    # Conditional routing from triage
    def triage_routing(state: AgentState):
        """Route based on triage confidence score."""
        confidence = state.get("confidence_score", 0)
        if confidence > 0.7:
            return "rag"  # High confidence → proceed to RAG
        else:
            return "ask_info"  # Low confidence → ask for more info

    workflow.add_conditional_edges(
        "triage",
        triage_routing,
        {
            "rag": "rag",
            "ask_info": "ask_info"
        }
    )

    # After asking for info, go back to triage for re-analysis
    workflow.add_edge("ask_info", "triage")

    # Normal flow: RAG → Planner → Feedback → END
    workflow.add_edge("rag", "planner")
    workflow.add_edge("planner", "feedback")
    workflow.add_edge("feedback", END)

    return workflow.compile()