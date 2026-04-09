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
    dtc_list: list[str], model: str = None, model_year: int = None, firmware: str = None
):
    """
    Lookup diagnostics in SQLite by candidate DTC list and context metadata.
    If dtc_list is empty, fallback to all diagnostics matching context.
    """
    diagnostics = []
    with sqlite3.connect(DB_PATH) as conn:
        if model and model_year is not None and firmware:
            firmware_rows = conn.execute(
                """
                SELECT COUNT(*) FROM diagnostic_manual
                WHERE model = ? AND model_year = ? AND firmware = ?
                """,
                (model, int(model_year), firmware),
            ).fetchone()[0]
        else:
            firmware_rows = 0

        if dtc_list:
            placeholders = ",".join("?" for _ in dtc_list)
            if model and model_year is not None and firmware_rows > 0 and firmware:
                rows = conn.execute(
                    f"""
                    SELECT dtc, description, possible_causes_json, diagnostic_steps_json
                    FROM diagnostic_manual
                    WHERE model = ? AND model_year = ? AND firmware = ?
                      AND dtc IN ({placeholders})
                    """,
                    (model, int(model_year), firmware, *dtc_list),
                ).fetchall()
            elif model and model_year is not None:
                rows = conn.execute(
                    f"""
                    SELECT dtc, description, possible_causes_json, diagnostic_steps_json
                    FROM diagnostic_manual
                    WHERE model = ? AND model_year = ?
                      AND dtc IN ({placeholders})
                    """,
                    (model, int(model_year), *dtc_list),
                ).fetchall()
            elif model:
                rows = conn.execute(
                    f"""
                    SELECT dtc, description, possible_causes_json, diagnostic_steps_json
                    FROM diagnostic_manual
                    WHERE model = ? AND dtc IN ({placeholders})
                    """,
                    (model, *dtc_list),
                ).fetchall()
            else:
                rows = conn.execute(
                    f"""
                    SELECT dtc, description, possible_causes_json, diagnostic_steps_json
                    FROM diagnostic_manual
                    WHERE dtc IN ({placeholders})
                    """,
                    (*dtc_list,),
                ).fetchall()
            by_dtc = {
                row[0]: {
                    "dtc": row[0],
                    "description": row[1],
                    "possible_causes": json.loads(row[2]) if row[2] else [],
                    "diagnostic_steps": json.loads(row[3]) if row[3] else [],
                }
                for row in rows
            }
            for dtc in dtc_list:
                diagnostics.append(
                    by_dtc.get(
                        dtc,
                        {
                            "dtc": dtc,
                            "description": "",
                            "possible_causes": [],
                            "diagnostic_steps": [],
                        },
                    )
                )
        else:
            if model and model_year is not None and firmware_rows > 0 and firmware:
                rows = conn.execute(
                    """
                    SELECT dtc, description, possible_causes_json, diagnostic_steps_json
                    FROM diagnostic_manual
                    WHERE model = ? AND model_year = ? AND firmware = ?
                    """,
                    (model, int(model_year), firmware),
                ).fetchall()
            elif model and model_year is not None:
                rows = conn.execute(
                    """
                    SELECT dtc, description, possible_causes_json, diagnostic_steps_json
                    FROM diagnostic_manual
                    WHERE model = ? AND model_year = ?
                    """,
                    (model, int(model_year)),
                ).fetchall()
            elif model:
                rows = conn.execute(
                    """
                    SELECT dtc, description, possible_causes_json, diagnostic_steps_json
                    FROM diagnostic_manual
                    WHERE model = ?
                    """,
                    (model,),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT dtc, description, possible_causes_json, diagnostic_steps_json
                    FROM diagnostic_manual
                    """,
                ).fetchall()
            for row in rows:
                diagnostics.append(
                    {
                        "dtc": row[0],
                        "description": row[1],
                        "possible_causes": json.loads(row[2]) if row[2] else [],
                        "diagnostic_steps": json.loads(row[3]) if row[3] else [],
                    }
                )

    return {"diagnostics": diagnostics}
