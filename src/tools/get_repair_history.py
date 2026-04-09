from langchain_core.tools import tool
import json

REPAIR_HISTORY_FILE = "C:\\Users\\NCQHuy\\Desktop\\AIThucChien\\LopSang\\Day6\\lab05_c401_a2\\src\\data\\repair_history.json"

@tool
def get_repair_history(model: str = None, model_year: int = None, firmware: str = None):
    """
    Retrieve repair history based on vehicle metadata.
    Used to identify common issues and fixes for similar vehicles.
    """

    with open(REPAIR_HISTORY_FILE, "r") as f:
        repair_history = json.load(f)

    results = []
    for r in repair_history:
        vehicle = r.get("vehicle", {})
        fw = r.get("firmware")

        if model and vehicle.get("model") != model:
            continue

        if model_year and vehicle.get("model_year") != model_year:
            continue

        if firmware and fw != firmware:
            continue

        results.append(r)

    return results