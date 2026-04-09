from langchain_core.tools import tool
import json
import os
import sqlite3
from pathlib import Path

DB_PATH = os.getenv(
    "STRUCTURE_DB_PATH",
    str(Path(__file__).resolve().parents[1] / "data" / "structure_database.db"),
)


@tool
def get_diagnostic(
    dtc_list: list[str] | None = None,
    model: str | None = None,
    model_year: int | None = None,
    firmware: str | None = None,
):
    """
    Lookup diagnostics in SQLite by DTC list and optional context metadata.
    If dtc_list is empty, return all diagnostics matching the context.
    """

    dtc_list = dtc_list or []

    query = """
        SELECT dtc, description, possible_causes_json, diagnostic_steps_json
        FROM diagnostic_manual
    """

    conditions = []
    params = []

    # Add context filters
    if model:
        conditions.append("model = ?")
        params.append(model)

    if model_year is not None:
        conditions.append("model_year = ?")
        params.append(int(model_year))

    # Only apply firmware if provided
    if firmware:
        conditions.append("firmware = ?")
        params.append(firmware)

    # Add DTC filter
    if dtc_list:
        placeholders = ",".join("?" for _ in dtc_list)
        conditions.append(f"dtc IN ({placeholders})")
        params.extend(dtc_list)

    # Build final query
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    diagnostics = []

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(query, params).fetchall()

    by_dtc = {
        row[0]: {
            "dtc": row[0],
            "description": row[1],
            "possible_causes": json.loads(row[2]) if row[2] else [],
            "diagnostic_steps": json.loads(row[3]) if row[3] else [],
        }
        for row in rows
    }

    # Preserve original DTC order if dtc_list is provided
    if dtc_list:
        diagnostics = [
            by_dtc.get(
                dtc,
                {
                    "dtc": dtc,
                    "description": "",
                    "possible_causes": [],
                    "diagnostic_steps": [],
                },
            )
            for dtc in dtc_list
        ]
    else:
        diagnostics = list(by_dtc.values())

    return {"diagnostics": diagnostics}
