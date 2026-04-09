import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any


REQUIRED_REPAIR_KEYS = {
    "vehicle",
    "symptom",
    "observed_dtc",
    "root_cause",
    "fix",
    "parts_replaced",
    "time_to_repair_min",
    "result",
    "rework",
}
REQUIRED_VEHICLE_KEYS = {"model", "model_year", "firmware"}

REQUIRED_DIAGNOSTIC_KEYS = {
    "dtc",
    "description",
    "applicable",
    "possible_causes",
    "diagnostic_steps",
}
REQUIRED_APPLICABLE_KEYS = {"model", "model_year", "firmware"}


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    project_src_dir = script_dir.parent
    data_dir = project_src_dir / "data"

    parser = argparse.ArgumentParser(
        description="Load Repair History + Diagnostic Manual JSON data into SQLite."
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=project_src_dir / "data" / "structure_database.db",
        help="Path to output SQLite database file.",
    )
    parser.add_argument(
        "--repair-json",
        type=Path,
        default=data_dir / "repair_history.json",
        help="Path to repair_history.json file.",
    )
    parser.add_argument(
        "--diagnostic-json",
        type=Path,
        default=data_dir / "diagnostic_manual.json",
        help="Path to diagnostic_manual.json file.",
    )
    return parser.parse_args()


def load_json_list(path: Path, name: str) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"{name} file not found: {path}")

    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)

    if not isinstance(data, list):
        raise ValueError(f"{name} must be a JSON array, got: {type(data).__name__}")

    if not all(isinstance(item, dict) for item in data):
        raise ValueError(f"{name} must contain only JSON objects")

    return data


def _missing_keys(record: dict[str, Any], required: set[str]) -> list[str]:
    return sorted(key for key in required if key not in record)


def validate_repair_record(record: dict[str, Any], idx: int) -> None:
    missing = _missing_keys(record, REQUIRED_REPAIR_KEYS)
    if missing:
        raise ValueError(f"repair_history[{idx}] missing keys: {missing}")

    vehicle = record["vehicle"]
    if not isinstance(vehicle, dict):
        raise ValueError(f"repair_history[{idx}].vehicle must be object")

    vehicle_missing = _missing_keys(vehicle, REQUIRED_VEHICLE_KEYS)
    if vehicle_missing:
        raise ValueError(f"repair_history[{idx}].vehicle missing keys: {vehicle_missing}")


def validate_diagnostic_record(record: dict[str, Any], idx: int) -> None:
    missing = _missing_keys(record, REQUIRED_DIAGNOSTIC_KEYS)
    if missing:
        raise ValueError(f"diagnostic_manual[{idx}] missing keys: {missing}")

    applicable = record["applicable"]
    if not isinstance(applicable, dict):
        raise ValueError(f"diagnostic_manual[{idx}].applicable must be object")

    applicable_missing = _missing_keys(applicable, REQUIRED_APPLICABLE_KEYS)
    if applicable_missing:
        raise ValueError(
            f"diagnostic_manual[{idx}].applicable missing keys: {applicable_missing}"
        )


def create_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS repair_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            model_year INTEGER NOT NULL,
            firmware TEXT NOT NULL,
            symptom TEXT NOT NULL,
            observed_dtc TEXT NOT NULL,
            root_cause TEXT NOT NULL,
            fix TEXT NOT NULL,
            parts_replaced_json TEXT NOT NULL,
            time_to_repair_min INTEGER NOT NULL,
            result TEXT NOT NULL,
            rework INTEGER NOT NULL CHECK (rework IN (0, 1)),
            raw_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_repair_history_dtc
            ON repair_history(observed_dtc);
        CREATE INDEX IF NOT EXISTS idx_repair_history_vehicle
            ON repair_history(model, model_year, firmware);

        CREATE TABLE IF NOT EXISTS diagnostic_manual (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dtc TEXT NOT NULL,
            description TEXT NOT NULL,
            model TEXT NOT NULL,
            model_year INTEGER NOT NULL,
            firmware TEXT NOT NULL,
            possible_causes_json TEXT NOT NULL,
            diagnostic_steps_json TEXT NOT NULL,
            raw_json TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_diagnostic_manual_dtc
            ON diagnostic_manual(dtc);
        CREATE INDEX IF NOT EXISTS idx_diagnostic_manual_vehicle
            ON diagnostic_manual(model, model_year, firmware);
        """
    )


def insert_repair_history(
    conn: sqlite3.Connection, repair_history_data: list[dict[str, Any]]
) -> int:
    rows = []
    for idx, record in enumerate(repair_history_data):
        validate_repair_record(record, idx)

        vehicle = record["vehicle"]
        rows.append(
            (
                vehicle["model"],
                int(vehicle["model_year"]),
                vehicle["firmware"],
                record["symptom"],
                record["observed_dtc"],
                record["root_cause"],
                record["fix"],
                json.dumps(record["parts_replaced"], ensure_ascii=False),
                int(record["time_to_repair_min"]),
                record["result"],
                int(bool(record["rework"])),
                json.dumps(record, ensure_ascii=False),
            )
        )

    conn.execute("DELETE FROM repair_history")
    conn.executemany(
        """
        INSERT INTO repair_history (
            model, model_year, firmware, symptom, observed_dtc, root_cause, fix,
            parts_replaced_json, time_to_repair_min, result, rework, raw_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    return len(rows)


def insert_diagnostic_manual(
    conn: sqlite3.Connection, diagnostic_data: list[dict[str, Any]]
) -> int:
    rows = []
    for idx, record in enumerate(diagnostic_data):
        validate_diagnostic_record(record, idx)

        applicable = record["applicable"]
        rows.append(
            (
                record["dtc"],
                record["description"],
                applicable["model"],
                int(applicable["model_year"]),
                applicable["firmware"],
                json.dumps(record["possible_causes"], ensure_ascii=False),
                json.dumps(record["diagnostic_steps"], ensure_ascii=False),
                json.dumps(record, ensure_ascii=False),
            )
        )

    conn.execute("DELETE FROM diagnostic_manual")
    conn.executemany(
        """
        INSERT INTO diagnostic_manual (
            dtc, description, model, model_year, firmware,
            possible_causes_json, diagnostic_steps_json, raw_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    return len(rows)


def main() -> None:
    args = parse_args()
    args.db.parent.mkdir(parents=True, exist_ok=True)

    repair_history_data = load_json_list(args.repair_json, "repair_history")
    diagnostic_data = load_json_list(args.diagnostic_json, "diagnostic_manual")

    with sqlite3.connect(args.db) as conn:
        create_tables(conn)
        repair_count = insert_repair_history(conn, repair_history_data)
        diagnostic_count = insert_diagnostic_manual(conn, diagnostic_data)
        conn.commit()

    print(f"Loaded SQLite DB: {args.db}")
    print(f"- repair_history: {repair_count} rows")
    print(f"- diagnostic_manual: {diagnostic_count} rows")


if __name__ == "__main__":
    main()
