import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Optional

import requests


REQUIRED_DOC_KEYS = {"document_id", "metadata", "content"}
REQUIRED_METADATA_KEYS = {"model", "model_year", "firmware", "section"}
ALLOWED_DISTANCE = {"Cosine", "Dot", "Euclid", "Manhattan"}


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(
        description="Load service_manual.json into Qdrant vector DB."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=script_dir / "vector_db_config.json",
        help="Path to vector ingestion config JSON file.",
    )
    parser.add_argument(
        "--service-json",
        type=Path,
        default=None,
        help="Path to service_manual.json file.",
    )
    parser.add_argument(
        "--collection",
        type=str,
        default=None,
        help="Qdrant collection name.",
    )
    parser.add_argument(
        "--vector-size",
        type=int,
        default=None,
        help="Vector size used for generated embeddings.",
    )
    parser.add_argument(
        "--distance",
        type=str,
        default=None,
        choices=sorted(ALLOWED_DISTANCE),
        help="Distance metric for Qdrant collection.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=None,
        help="How many points to upsert per request.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only validate/prepare data, do not call Qdrant APIs.",
    )
    return parser.parse_args()


def load_service_manual(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"service_manual file not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"service_manual must be a JSON array, got: {type(data).__name__}")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("service_manual must contain only JSON objects")

    return data


def load_json_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Config must be a JSON object, got: {type(data).__name__}")
    return data


def resolve_runtime_config(args: argparse.Namespace) -> dict[str, Any]:
    script_dir = Path(__file__).resolve().parent
    project_src_dir = script_dir.parent

    cfg = load_json_config(args.config)

    service_json_raw = args.service_json or cfg.get("service_json", "data/service_manual.json")
    service_json = Path(service_json_raw)
    if not service_json.is_absolute():
        service_json = project_src_dir / service_json

    collection = args.collection or cfg.get("collection", "service_manual")
    vector_size = args.vector_size or int(cfg.get("vector_size", 384))
    distance = args.distance or cfg.get("distance", "Cosine")
    batch_size = args.batch_size or int(cfg.get("batch_size", 64))

    if distance not in ALLOWED_DISTANCE:
        raise ValueError(f"Invalid distance '{distance}', expected one of {sorted(ALLOWED_DISTANCE)}")

    if vector_size <= 0:
        raise ValueError("vector_size must be > 0")
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")

    return {
        "service_json": service_json,
        "collection": collection,
        "vector_size": vector_size,
        "distance": distance,
        "batch_size": batch_size,
        "config_path": args.config,
    }


def _missing_keys(record: dict[str, Any], required: set[str]) -> list[str]:
    return sorted(key for key in required if key not in record)


def validate_service_record(record: dict[str, Any], idx: int) -> None:
    missing = _missing_keys(record, REQUIRED_DOC_KEYS)
    if missing:
        raise ValueError(f"service_manual[{idx}] missing keys: {missing}")

    metadata = record["metadata"]
    if not isinstance(metadata, dict):
        raise ValueError(f"service_manual[{idx}].metadata must be object")

    metadata_missing = _missing_keys(metadata, REQUIRED_METADATA_KEYS)
    if metadata_missing:
        raise ValueError(f"service_manual[{idx}].metadata missing keys: {metadata_missing}")

    if not isinstance(record["content"], str) or not record["content"].strip():
        raise ValueError(f"service_manual[{idx}].content must be a non-empty string")


def _to_point_id(document_id: str) -> str:
    # Stable UUID-like ID derived from document_id.
    digest = hashlib.md5(document_id.encode("utf-8")).hexdigest()
    return f"{digest[:8]}-{digest[8:12]}-{digest[12:16]}-{digest[16:20]}-{digest[20:32]}"


def _hash_embedding(text: str, size: int) -> list[float]:
    # Deterministic dependency-free embedding.
    vec = [0.0] * size
    for token in text.lower().split():
        h = hashlib.blake2b(token.encode("utf-8"), digest_size=16).digest()
        idx = int.from_bytes(h[:4], "big") % size
        sign = 1.0 if (h[4] % 2 == 0) else -1.0
        vec[idx] += sign

    norm_sq = sum(v * v for v in vec)
    if norm_sq == 0:
        return vec

    norm = norm_sq ** 0.5
    return [v / norm for v in vec]


def build_points(docs: list[dict[str, Any]], vector_size: int) -> list[dict[str, Any]]:
    points: list[dict[str, Any]] = []

    for idx, doc in enumerate(docs):
        validate_service_record(doc, idx)
        text_for_embedding = f"{doc['metadata']['section']}\n{doc['content']}"

        points.append(
            {
                "id": _to_point_id(str(doc["document_id"])),
                "vector": _hash_embedding(text_for_embedding, vector_size),
                "payload": {
                    "document_id": doc["document_id"],
                    "metadata": doc["metadata"],
                    "content": doc["content"],
                },
            }
        )

    return points


class QdrantRestClient:
    def __init__(self, base_url: str, api_key: Optional[str]):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["api-key"] = api_key

    def _request(
        self, method: str, path: str, payload: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        response = requests.request(
            method=method,
            url=f"{self.base_url}{path}",
            headers=self.headers,
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        return response.json() if response.text else {}

    def collection_exists(self, collection: str) -> bool:
        response = requests.get(
            f"{self.base_url}/collections/{collection}",
            headers=self.headers,
            timeout=30,
        )
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True

    def create_collection(self, collection: str, vector_size: int, distance: str) -> None:
        self._request(
            "PUT",
            f"/collections/{collection}",
            {
                "vectors": {
                    "size": vector_size,
                    "distance": distance,
                }
            },
        )

    def upsert_points(self, collection: str, points: list[dict[str, Any]]) -> None:
        self._request(
            "PUT",
            f"/collections/{collection}/points",
            {
                "points": points,
                "wait": True,
            },
        )


def chunked(items: list[dict[str, Any]], batch_size: int) -> list[list[dict[str, Any]]]:
    return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def main() -> None:
    args = parse_args()
    runtime = resolve_runtime_config(args)
    load_env_file(Path(__file__).resolve().parent.parent / ".env")

    docs = load_service_manual(runtime["service_json"])
    points = build_points(docs, runtime["vector_size"])

    if args.dry_run:
        print("Dry-run completed (no Qdrant API call).")
        print(f"- config: {runtime['config_path']}")
        print(f"- documents validated: {len(docs)}")
        print(f"- points prepared: {len(points)}")
        print(f"- collection: {runtime['collection']}")
        print(f"- vector_size: {runtime['vector_size']}")
        print(f"- distance: {runtime['distance']}")
        print(f"- batch_size: {runtime['batch_size']}")
        return

    base_url = os.getenv("QDRANT_BASE_URL")
    api_key = os.getenv("QDRANT_API_KEY")
    if not base_url:
        raise ValueError("Missing QDRANT_BASE_URL in .env")

    client = QdrantRestClient(base_url=base_url, api_key=api_key)

    if not client.collection_exists(runtime["collection"]):
        client.create_collection(
            runtime["collection"], runtime["vector_size"], runtime["distance"]
        )

    total_upserted = 0
    for batch in chunked(points, runtime["batch_size"]):
        client.upsert_points(runtime["collection"], batch)
        total_upserted += len(batch)

    print("Qdrant ingestion completed.")
    print(f"- config: {runtime['config_path']}")
    print(f"- collection: {runtime['collection']}")
    print(f"- documents loaded: {total_upserted}")


if __name__ == "__main__":
    main()
