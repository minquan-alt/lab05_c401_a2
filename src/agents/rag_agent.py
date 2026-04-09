import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from concurrent.futures import ThreadPoolExecutor, as_completed
from graph.state import AgentState
from tools.mock_tools import get_sm_details, get_kb_insights, get_system_procedures
from llm_config import get_llm, get_llm_response_text
from workflow_logger import workflow_logger, log_agent_input, log_agent_output
from system_prompts import get_rag_prompt

def rag_agent(state: AgentState) -> AgentState:
    """Retrieve and reason with information from SM and KB."""
    
    # Log agent start
    workflow_logger.section("RAG AGENT")
    state["current_stage"] = "rag"
    log_agent_input("RAG", {
        "symptom": state["symptom"],
        "probable_dtcs": state.get("probable_dtcs", [])
    })
    
    # Get LLM
    llm = get_llm()
    workflow_logger.info(f"LLM initialized: {type(llm).__name__}")
    
    # CROSS-RETRIEVAL STRATEGY
    retrieved = []
    probable_dtcs = state.get("probable_dtcs", [])

    if probable_dtcs:
        # DTC-BASED RETRIEVAL: When DTCs are available
        workflow_logger.section("DTC-BASED RETRIEVAL")
        workflow_logger.info(f"Found {len(probable_dtcs)} probable DTCs, retrieving SM data...")

        def fetch_sm_data(dtc):
            workflow_logger.tool_call("get_sm_details", {"dtc_code": dtc["code"]})
            sm_info = get_sm_details(dtc["code"])
            return dtc, sm_info

        with ThreadPoolExecutor(max_workers=min(4, len(probable_dtcs))) as executor:
            futures = {executor.submit(fetch_sm_data, dtc): dtc for dtc in probable_dtcs}
            for future in as_completed(futures):
                dtc, sm_info = future.result()
                if sm_info:
                    retrieved.append(f"SM_DTC: {dtc['code']} - {sm_info}")
                    workflow_logger.tool_result("get_sm_details", {"status": "Found", "dtc": dtc["code"]})
                    workflow_logger.state_update(f"SM Data for {dtc['code']}", str(sm_info)[:100])
                else:
                    workflow_logger.warning(f"No SM data found for {dtc['code']}")
    else:
        # SYSTEM-BASED RETRIEVAL: When no DTCs, use general procedures
        workflow_logger.section("SYSTEM-BASED RETRIEVAL")
        workflow_logger.info("No DTCs available, retrieving general system procedures...")

        # Extract suspected systems from symptom (simple keyword matching for now)
        suspected_systems = []
        symptom_lower = state["symptom"].lower()
        if any(word in symptom_lower for word in ["charge", "sạc", "charging"]):
            suspected_systems.append("charging")
        if any(word in symptom_lower for word in ["battery", "pin", "ắc quy"]):
            suspected_systems.append("battery")
        if any(word in symptom_lower for word in ["motor", "động cơ", "power"]):
            suspected_systems.append("motor")

        if suspected_systems:
            workflow_logger.tool_call("get_system_procedures", {"suspected_systems": suspected_systems})
            system_procedures = get_system_procedures(suspected_systems)
            workflow_logger.tool_result("get_system_procedures", {"procedures_found": len(system_procedures)})

            for proc in system_procedures:
                retrieved.append(f"PROCEDURE: {proc}")
                workflow_logger.state_update(f"Procedure: {proc['title']}", f"{len(proc['steps'])} steps")
        else:
            workflow_logger.warning("Could not identify suspected systems from symptom")

    # Always get KB insights for additional context
    workflow_logger.section("Retrieving Knowledge Base Data")
    workflow_logger.tool_call("get_kb_insights", {"symptom": state["symptom"]})
    kb_info = get_kb_insights(state["symptom"])
    workflow_logger.tool_result("get_kb_insights", {"count": len(kb_info)})

    for i, item in enumerate(kb_info):
        retrieved.append(f"KB: {item}")
        workflow_logger.state_update(f"KB Item {i+1}", str(item)[:100])

    state["retrieved_info"] = retrieved
    
    # Log retrieved data summary
    workflow_logger.info(f"\n📊 Data Summary:")
    workflow_logger.info(f"   Service Manual entries: {len([x for x in retrieved if x.startswith('SM:')])}")
    workflow_logger.info(f"   Knowledge Base entries: {len([x for x in retrieved if x.startswith('KB:')])}")
    
    # Use LLM to synthesize information
    workflow_logger.section("Synthesizing Data with LLM")
    rag_prompt = get_rag_prompt(state["symptom"], state["probable_dtcs"], "\n".join(retrieved))
    
    workflow_logger.tool_call("LLM_Synthesis", {
        "model": type(llm).__name__,
        "retrieved_items": len(retrieved)
    })
    
    # Invoke LLM directly with formatted prompt
    try:
        response = llm.invoke(rag_prompt)
    except Exception as e:
        workflow_logger.warning(f"LLM invoke failed: {e}. Retrying with Ollama local model.")
        from llm_config import get_ollama_llm
        llm = get_ollama_llm()
        response = llm.invoke(rag_prompt)

    response_text = get_llm_response_text(response)

    # Log synthesis result
    workflow_logger.tool_result("LLM_Synthesis", {"content": response_text[:200]})
    workflow_logger.reasoning("RAG", response_text[:300])

    # Add synthesis to retrieved_info
    state["retrieved_info"].append(f"Synthesis: {response_text}")
    
    # Log output
    log_agent_output("RAG", {
        "retrieved_info_count": len(state["retrieved_info"]),
        "synthesis": response_text[:150]
    })
    
    return state