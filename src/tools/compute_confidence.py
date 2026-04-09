from langchain_core.tools import tool


@tool
def compute_confidence(candidates: list[dict], diagnostics: list[dict]):
    """
    Decide confidence using history probability + diagnostic clarity.
    Rule:
    - high when top candidate prob > 0.7 and selected diagnostic has actionable data
    - otherwise low
    """
    ranked = sorted(
        [
            {"dtc": c.get("dtc"), "probability": float(c.get("probability", 0.0))}
            for c in (candidates or [])
            if c.get("dtc")
        ],
        key=lambda x: x["probability"],
        reverse=True,
    )

    if not ranked:
        return {
            "decision": "low",
            "selected_dtc": None,
            "ranked_candidates": [],
        }

    selected_dtc = ranked[0]["dtc"]
    top_prob = ranked[0]["probability"]

    selected_diag = next((d for d in (diagnostics or []) if d.get("dtc") == selected_dtc), None)
    has_diagnostic_detail = bool(
        selected_diag
        and selected_diag.get("possible_causes")
        and selected_diag.get("diagnostic_steps")
    )

    decision = "high" if (top_prob > 0.7 and has_diagnostic_detail) else "low"
    return {
        "decision": decision,
        "selected_dtc": selected_dtc if decision == "high" else None,
        "ranked_candidates": ranked,
    }
