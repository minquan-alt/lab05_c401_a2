from langchain_core.tools import tool
import sqlite3
import os
from pathlib import Path
from collections import Counter
import re

DB_PATH = os.getenv(
    "STRUCTURE_DB_PATH",
    str(Path(__file__).resolve().parents[1] / "data" / "structure_database.db"),
)

SYMPTOM_ALIASES = {
    "không sạc": "charge",
    "sạc": "charge",
    "trạm ac": "ac station",
    "lỗi pin": "battery warning",
    "báo lỗi pin": "battery warning",
    "pin": "battery",
    "giảm công suất": "reduced power",
    "quạt làm mát": "cooling fan",
    "quạt": "fan",
}


def _normalize_text(text: str) -> str:
    normalized = (text or "").lower()
    for vn, en in SYMPTOM_ALIASES.items():
        normalized = normalized.replace(vn, en)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized

@tool
def get_repair_history(
    symptom: str, model: str = None, model_year: int = None, firmware: str = None
):
    """
    Retrieve DTC candidates from SQLite repair_history table.
    Matching strategy:
    - mandatory filter by model/model_year
    - optional firmware filter (derived from symptom text if present)
    - symptom token overlap filtering
    - probability from frequency over matched rows
    """
    symptom_norm = _normalize_text(str(symptom))
    symptom_tokens = set(symptom_norm.split())
    base_query = """
        SELECT model, model_year, firmware, symptom, observed_dtc, root_cause, fix,
               parts_replaced_json, time_to_repair_min, result, rework
        FROM repair_history
    """

    def _fetch_rows(use_model: bool, use_year: bool, use_firmware: bool):
        where = []
        params = []
        if use_model and model:
            where.append("model = ?")
            params.append(model)
        if use_year and model_year is not None:
            where.append("model_year = ?")
            params.append(int(model_year))
        if use_firmware and firmware:
            where.append("firmware = ?")
            params.append(firmware)

        query = base_query
        if where:
            query += " WHERE " + " AND ".join(where)
        with sqlite3.connect(DB_PATH) as conn:
            return conn.execute(query, tuple(params)).fetchall()

    # Query strategy: strict -> progressively relax filters to still provide candidates.
    rows = _fetch_rows(True, True, True)
    if not rows:
        rows = _fetch_rows(True, True, False)
    if not rows:
        rows = _fetch_rows(True, False, False)
    if not rows:
        rows = _fetch_rows(False, True, False)
    if not rows:
        rows = _fetch_rows(False, False, False)

    matched = []
    for row in rows:
        case_symptom = _normalize_text(str(row[3] or ""))
        if not case_symptom:
            continue
        case_tokens = set(case_symptom.split())
        overlap = len(symptom_tokens & case_tokens)
        if overlap == 0 and symptom_norm not in case_symptom and case_symptom not in symptom_norm:
            continue
        matched.append(
            {
                "model": row[0],
                "model_year": row[1],
                "firmware": row[2],
                "symptom": row[3],
                "observed_dtc": row[4],
                "root_cause": row[5],
                "fix": row[6],
                "parts_replaced_json": row[7],
                "time_to_repair_min": row[8],
                "result": row[9],
                "rework": bool(row[10]),
            }
        )

    if not matched:
        return {"candidates": [], "records": []}

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
    return {"candidates": ranked[:3], "records": matched}
