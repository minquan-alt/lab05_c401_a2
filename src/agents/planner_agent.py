import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.state import AgentState
from tools.mock_tools import verify_safety_standards
from llm_config import get_llm, get_llm_response_text
from workflow_logger import workflow_logger, log_agent_input, log_agent_output
from system_prompts import get_planner_prompt

def planner_agent(state: AgentState) -> AgentState:
    """Generate repair plan and checklist."""
    
    # Log agent start
    workflow_logger.section("PLANNER AGENT")
    state["current_stage"] = "planner"
    log_agent_input("PLANNER", {
        "symptom": state["symptom"],
        "retrieved_info_count": len(state.get("retrieved_info", []))
    })
    
    # Get LLM
    llm = get_llm()
    workflow_logger.info(f"LLM initialized: {type(llm).__name__}")
    
    # Retrieve safety standards
    workflow_logger.section("Loading Safety Standards")
    workflow_logger.tool_call("verify_safety_standards", {})
    safety_standards = verify_safety_standards()
    workflow_logger.tool_result("verify_safety_standards", {"count": len(safety_standards)})
    
    for i, standard in enumerate(safety_standards):
        workflow_logger.info(f"   [{i+1}] {standard}")
    
    # Create planner prompt
    diagnosis_summary = "\n".join(state.get("retrieved_info", [])[-3:])  # Last 3 items
    planner_prompt = get_planner_prompt(diagnosis_summary, safety_standards)
    
    # Log tool call
    workflow_logger.section("Generating Repair Plan")
    workflow_logger.tool_call("LLM_PlanGeneration", {
        "model": type(llm).__name__,
        "safety_standards_count": len(safety_standards),
        "info_items": len(state.get("retrieved_info", []))
    })
    
    # Invoke LLM directly with formatted prompt
    try:
        response = llm.invoke(planner_prompt)
    except Exception as e:
        workflow_logger.warning(f"LLM invoke failed: {e}. Retrying with Ollama local model.")
        from llm_config import get_ollama_llm
        llm = get_ollama_llm()
        response = llm.invoke(planner_prompt)

    response_text = get_llm_response_text(response)

    # Log result
    workflow_logger.tool_result("LLM_PlanGeneration", {"content": response_text[:200]})
    workflow_logger.reasoning("PLANNER", response_text[:300])

    state["repair_plan"] = response_text
    
    # Log output
    log_agent_output("PLANNER", {
        "repair_plan_length": len(response_text),
        "plan_preview": response_text[:100]
    })
    
    workflow_logger.success("Repair plan generated successfully")
    
    return state