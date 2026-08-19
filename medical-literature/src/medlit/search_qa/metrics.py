from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any


def _ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 6) if denominator else 0.0


def compute_metrics(*, formal_count: int, challenger_intersection: int, challenger_unique: int, verified_count: int, unresolved_doi: int, dedup_review: int, trial_links: int, trials: int, citation_unique: int, citation_total: int) -> dict[str, float]:
    return {
        "known_item_recall": 0.0,
        "formal_challenger_overlap": _ratio(challenger_intersection, formal_count),
        "citation_unique_rate": _ratio(citation_unique, citation_total),
        "trial_publication_link_rate": _ratio(trial_links, trials),
        "identifier_verification_rate": _ratio(verified_count, formal_count),
        "unresolved_doi_rate": _ratio(unresolved_doi, formal_count),
        "dedup_review_rate": _ratio(dedup_review, formal_count),
        "challenger_unique_count": float(challenger_unique),
    }


def build_freeze_manifest(*, freeze_id: str, databases: dict[str, dict[str, Any]], dedup_count: int, citation_snowball_count: int, challenger_unique_reviewed: int, known_item_recall: float, reviewer: str) -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "freeze_id": freeze_id,
        "date": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "databases": sorted(databases),
        "queries": {name: data.get("query") for name, data in databases.items()},
        "trial_registries": [],
        "upstream_versions": {},
        "result_counts": {name: data.get("count") for name, data in databases.items()},
        "dedup_count": dedup_count,
        "citation_snowball_count": citation_snowball_count,
        "challenger_unique_reviewed": challenger_unique_reviewed,
        "known_item_recall": known_item_recall,
        "reviewer": reviewer,
    }
    digest = hashlib.sha256(json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    manifest["sha256"] = digest
    return manifest
