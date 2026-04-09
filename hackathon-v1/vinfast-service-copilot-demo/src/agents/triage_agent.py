import sys
import os
import json
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.state import AgentState
from llm_config import get_llm
from workflow_logger import workflow_logger, log_agent_input, log_agent_output
from system_prompts import get_triage_prompt
from tools.mock_tools import search_dtc_by_symptom

def extract_json_from_response(content: str) -> str:
    """Extract JSON from LLM response that may be wrapped in markdown code blocks."""
    # Remove markdown code block markers
    content = re.sub(r'```\w*\n?', '', content)
    content = content.strip()
    
    # Find JSON object boundaries
    start_idx = content.find('{')
    end_idx = content.rfind('}') + 1
    
    if start_idx != -1 and end_idx > start_idx:
        return content[start_idx:end_idx]
    
    return content

def triage_agent(state: AgentState) -> AgentState:
    """Analyze initial symptom using LLM reasoning and tool-based DTC lookup."""

    # Log agent start
    workflow_logger.section("TRIAGE AGENT")
    log_agent_input("TRIAGE", {"vin": state["vin"], "symptom": state["symptom"]})

    # Get LLM
    llm = get_llm()
    workflow_logger.info(f"LLM initialized: {type(llm).__name__}")

    # Create prompt with system instructions
    triage_prompt = get_triage_prompt(state["symptom"])

    # Log tool call
    workflow_logger.tool_call("LLM_Invoke", {
        "model": type(llm).__name__,
        "task": "Technical Signal Extraction"
    })

    # Invoke LLM to extract technical signals
    response = llm.invoke(triage_prompt)

    # Log LLM response
    workflow_logger.tool_result("LLM_Response", {"content": response.content[:200]})

    # Parse response
    try:
        # Extract JSON from response (handles markdown code blocks)
        json_content = extract_json_from_response(response.content)
        result = json.loads(json_content)

        suspected_systems = result.get("suspected_systems", [])
        technical_keywords = result.get("technical_keywords", [])

        # Use tool to search for DTCs based on extracted signals
        workflow_logger.tool_call("search_dtc_by_symptom", {
            "suspected_systems": suspected_systems,
            "technical_keywords": technical_keywords
        })

        probable_dtcs = search_dtc_by_symptom(suspected_systems, technical_keywords)

        workflow_logger.tool_result("search_dtc_by_symptom", {
            "found_dtcs": len(probable_dtcs),
            "systems_searched": suspected_systems
        })

        # Update state with results
        state["confidence_score"] = result.get("confidence_score", 0.5)
        state["next_action"] = result.get("next_action", "ask_more_info")
        state["probable_dtcs"] = probable_dtcs

        # Log confidence and reasoning
        workflow_logger.confidence(state["confidence_score"])
        workflow_logger.reasoning("TRIAGE", result.get("reasoning", "Analysis complete"))

        # Log DTCs found
        if probable_dtcs:
            workflow_logger.info(f"Probable DTCs identified: {[d['code'] for d in probable_dtcs]}")
            for dtc in probable_dtcs:
                workflow_logger.info(f"  {dtc['code']}: {dtc['description']} ({dtc['system']})")

        # Log questions if needed
        questions = result.get("questions_if_needed", [])
        if questions:
            workflow_logger.info("Additional information needed:")
            for q in questions:
                workflow_logger.info(f"  ❓ {q}")

    except json.JSONDecodeError as e:
        workflow_logger.warning(f"Failed to parse LLM response as JSON: {e}")
        state["confidence_score"] = 0.5
        state["next_action"] = "ask_more_info"
        state["probable_dtcs"] = []
    except Exception as e:
        workflow_logger.error(f"Triage agent error: {e}")
        state["confidence_score"] = 0.5
        state["next_action"] = "ask_more_info"
        state["probable_dtcs"] = []

    # Log output
    log_agent_output("TRIAGE", {
        "confidence_score": state["confidence_score"],
        "next_action": state["next_action"],
        "probable_dtcs_count": len(state["probable_dtcs"])
    })

    return state