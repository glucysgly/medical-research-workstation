"""Command-line artifact helpers with explicit, local-only I/O.

These helpers intentionally consume exported JSON and write run artifacts. They
do not authenticate to commercial databases, upload documents, or mutate a
Zotero library.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from medlit.adapters.verification.doi_fallback import evaluate_verification
from medlit.canonical.normalize import deduplicate_papers, normalize_paper
from medlit.domain.models import SourceRole
from medlit.orchestrator.offline import run_offline_pipeline
from medlit.search_qa.engine import compare_formal_challenger, source_overlap_matrix
from medlit.search_qa.metrics import build_freeze_manifest
from medlit.search_strategy.artifact import render_yaml


def load_json(path: str | Path) -> Any:
    """Read a UTF-8 JSON artifact and fail with a useful path-aware error."""

    input_path = Path(path)
    if not input_path.is_file():
        raise ValueError(f"input JSON does not exist: {input_path}")
    try:
        return json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {input_path}: {exc}") from exc


def _records(value: Any, *, label: str) -> list[dict[str, Any]]:
    records = value.get("records") if isinstance(value, dict) else value
    if not isinstance(records, list) or not all(isinstance(record, dict) for record in records):
        raise ValueError(f"{label} must be a JSON array of objects or an object with a records array")
    return records


def _normalize_records(records: list[dict[str, Any]], *, source: str, role: SourceRole, run_id: str) -> list[Any]:
    return [normalize_paper(record, source=source, source_role=role, run_id=run_id) for record in records]


def search_qa_from_json(formal_path: str | Path, challenger_path: str | Path) -> dict[str, Any]:
    """Compare formal and challenger exports without changing formal counts."""

    run_id = "cli-search-qa"
    formal = _normalize_records(_records(load_json(formal_path), label="formal JSON"), source="formal-import", role=SourceRole.FORMAL_DATABASE, run_id=run_id)
    challenger = _normalize_records(_records(load_json(challenger_path), label="challenger JSON"), source="challenger-import", role=SourceRole.CHALLENGER, run_id=run_id)
    combined, dedup_audit = deduplicate_papers([*formal, *challenger])
    qa = compare_formal_challenger(formal, challenger)
    qa["dedup_count"] = len(combined)
    qa["dedup_audit"] = dedup_audit
    return {
        "status": "READY",
        "formal_count": len(formal),
        "challenger_count": len(challenger),
        "qa": qa,
        "source_overlap": source_overlap_matrix({"formal": formal, "challenger": challenger}),
    }


def verify_from_json(path: str | Path) -> dict[str, Any]:
    """Verify one citation using provider records already exported locally."""

    value = load_json(path)
    if not isinstance(value, dict):
        raise ValueError("verification input must be a JSON object")
    required = ("title", "provider_records")
    missing = [field for field in required if field not in value]
    if missing:
        raise ValueError(f"verification input is missing: {', '.join(missing)}")
    if not isinstance(value["provider_records"], dict):
        raise ValueError("provider_records must be an object keyed by provider")
    result = evaluate_verification(
        title=str(value["title"]),
        doi=value.get("doi"),
        year=value.get("year"),
        authors=[str(author) for author in value.get("authors", [])],
        provider_records=value["provider_records"],
    )
    return {"status": "READY", "verification": result.to_dict()}


def freeze_from_json(input_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    """Build and persist the human-reviewed search freeze manifest."""

    value = load_json(input_path)
    if not isinstance(value, dict):
        raise ValueError("freeze input must be a JSON object")
    databases = value.get("databases")
    if not isinstance(databases, dict) or not databases:
        raise ValueError("freeze input requires a non-empty databases object")
    manifest = build_freeze_manifest(
        freeze_id=str(value.get("freeze_id") or "freeze-pending"),
        databases=databases,
        dedup_count=int(value.get("dedup_count", 0)),
        citation_snowball_count=int(value.get("citation_snowball_count", 0)),
        challenger_unique_reviewed=int(value.get("challenger_unique_reviewed", 0)),
        known_item_recall=float(value.get("known_item_recall", 0.0)),
        reviewer=str(value.get("reviewer") or "UNASSIGNED"),
    )
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_yaml(manifest), encoding="utf-8")
    return {"status": "READY", "output": str(destination), "manifest": manifest, "manifest_json": json.dumps(manifest, ensure_ascii=False, sort_keys=True)}


def offline_e2e(output_root: str | Path) -> dict[str, Any]:
    """Run the deterministic core E2E using clearly synthetic fixture records."""

    run = run_offline_pipeline(
        Path(output_root),
        question="offline synthetic cervical cancer fixture",
        formal_records=[
            {"pmid": "fixture-1", "title": "Synthetic formal paper", "year": 2024},
            {"doi": "10.5555/fixture-2", "title": "Synthetic second paper", "year": 2023},
        ],
        discovery_records=[
            {"doi": "10.5555/fixture-2", "title": "Synthetic second paper", "year": 2023},
            {"doi": "10.5555/fixture-3", "title": "Synthetic discovery paper", "year": 2022},
        ],
        challenger_records=[
            {"pmid": "fixture-1", "title": "Synthetic formal paper", "year": 2024},
            {"doi": "10.5555/fixture-4", "title": "Synthetic challenger paper", "year": 2021},
        ],
    )
    return {"status": "PASS_OFFLINE_CORE", **run, "scientific_claim": "synthetic fixture only; external provider chain remains pending"}
