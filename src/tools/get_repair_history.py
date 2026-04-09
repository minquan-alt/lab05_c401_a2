from langchain_core.tools import tool
import json
from pathlib import Path
from collections import Counter

REPAIR_HISTORY_FILE = Path(__file__).resolve().parents[1] / "data" / "repair_history.json"

@tool
def get_repair_history(symptom: str, model: str, model_year: int):
    """
    Retrieve DTC candidates from similar repair cases.
    Matching strategy:
    - mandatory filter by model/model_year
    - light semantic score by symptom token overlap
    - probability from frequency over matched pool
    """
    with open(REPAIR_HISTORY_FILE, "r", encoding="utf-8") as f:
        repair_history = json.load(f)

    symptom_tokens = set(str(symptom).lower().split())
    matched = []
    for r in repair_history:
        vehicle = r.get("vehicle", {})
        if vehicle.get("model") != model:
            continue
        if vehicle.get("model_year") != model_year:
            continue

        case_symptom = str(r.get("symptom", "")).lower()
        if not case_symptom:
            continue
        case_tokens = set(case_symptom.split())
        overlap = len(symptom_tokens & case_tokens)
        # Keep exact-ish symptom or at least partial overlap to avoid noisy pool.
        if overlap == 0 and symptom.lower() not in case_symptom and case_symptom not in symptom.lower():
            continue
        matched.append(r)

    if not matched:
        return {"candidates": []}

    dtc_counter = Counter(item.get("observed_dtc") for item in matched if item.get("observed_dtc"))
    total = sum(dtc_counter.values())
    ranked = sorted(
        (
            {"dtc": dtc, "probability": round(count / total, 4)}
            for dtc, count in dtc_counter.items()
        ),
        key=lambda x: x["probability"],
        reverse=True,
    )
    return {"candidates": ranked[:3]}
