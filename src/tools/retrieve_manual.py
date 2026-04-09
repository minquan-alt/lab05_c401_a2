from pathlib import Path
import json
from langchain_core.tools import tool


SERVICE_MANUAL_FILE = Path(__file__).resolve().parents[1] / "data" / "service_manual.json"


@tool
def retrieve_manual(query: str, model: str, model_year: int, firmware: str):
    """
    Retrieve service manual documents by metadata filter and keyword score.
    """
    with open(SERVICE_MANUAL_FILE, "r", encoding="utf-8") as f:
        docs = json.load(f)

    query_tokens = set(str(query).lower().split())
    filtered = []
    for doc in docs:
        metadata = doc.get("metadata", {})
        if (
            metadata.get("model") != model
            or metadata.get("model_year") != model_year
            or metadata.get("firmware") != firmware
        ):
            continue

        content = str(doc.get("content", ""))
        score = sum(1 for token in query_tokens if token in content.lower())
        filtered.append((score, doc))

    filtered.sort(key=lambda item: item[0], reverse=True)
    top_docs = []
    for _, doc in filtered[:3]:
        top_docs.append(
            {
                "content": doc.get("content", ""),
                "metadata": {"section": doc.get("metadata", {}).get("section", "Unknown")},
            }
        )

    return {"documents": top_docs}
