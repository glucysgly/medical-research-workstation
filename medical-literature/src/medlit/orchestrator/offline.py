from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from medlit.canonical.normalize import deduplicate_papers, normalize_paper
from medlit.domain.models import SourceRole
from medlit.search_qa.engine import compare_formal_challenger, source_overlap_matrix
from medlit.search_strategy.artifact import build_query_artifact, render_yaml


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _write_strategy(path: Path, question: str, query: str) -> None:
    artifact = build_query_artifact(
        question=question,
        review_type="discovery",
        framework="PCC",
        concepts=[{"name": "topic", "controlled_terms": [], "free_terms": [query]}],
        databases=["pubmed", "paper-search"],
        queries={"pubmed": query, "paper-search": query},
        trial_queries={"clinicaltrials": None},
        peer_review={"status": "DRAFT", "reviewer": None, "notes": "offline fixture run"},
    )
    path.write_text(render_yaml(artifact), encoding="utf-8")


def _write_overlap(path: Path, matrix: dict[str, Any]) -> None:
    sources = matrix["sources"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", *sources])
        for source in sources:
            writer.writerow([source, *[matrix["rows"][source][other] for other in sources]])


def run_offline_pipeline(
    root: Path,
    *,
    question: str,
    formal_records: Iterable[dict[str, Any]],
    discovery_records: Iterable[dict[str, Any]],
    challenger_records: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = Path(root) / "runs" / run_id
    for provider in ("pubmed", "paper-search", "challenger"):
        (run_dir / "raw" / provider).mkdir(parents=True, exist_ok=True)
    formal_raw = list(formal_records)
    discovery_raw = list(discovery_records)
    challenger_raw = list(challenger_records)
    (run_dir / "raw" / "pubmed" / "records.json").write_text(json.dumps(formal_raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (run_dir / "raw" / "paper-search" / "records.json").write_text(json.dumps(discovery_raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (run_dir / "raw" / "challenger" / "records.json").write_text(json.dumps(challenger_raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    formal = [normalize_paper(r, source="pubmed", source_role=SourceRole.FORMAL_DATABASE, run_id=run_id, query=question) for r in formal_raw]
    discovery = [normalize_paper(r, source="paper-search", source_role=SourceRole.DISCOVERY_ENGINE, run_id=run_id, query=question) for r in discovery_raw]
    challenger = [normalize_paper(r, source="challenger", source_role=SourceRole.CHALLENGER, run_id=run_id, query=question) for r in challenger_raw]
    combined, dedup_audit = deduplicate_papers([*formal, *discovery, *challenger])
    qa = compare_formal_challenger(formal, challenger)
    qa["run_id"] = run_id
    qa["dedup_count"] = len(combined)
    qa["dedup_audit"] = dedup_audit
    matrix = source_overlap_matrix({"pubmed": formal, "paper-search": discovery, "challenger": challenger})
    _write_strategy(run_dir / "search_strategy.yaml", question, question)
    _write_overlap(run_dir / "source_overlap.csv", matrix)
    (run_dir / "search_qa.json").write_text(json.dumps(qa, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = {"run_id": run_id, "question": question, "formal_count": len(formal), "discovery_count": len(discovery), "challenger_count": len(challenger), "dedup_count": len(combined), "known_item_recall": None}
    manifest_bytes = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    manifest["sha256"] = hashlib.sha256(manifest_bytes).hexdigest()
    (run_dir / "run_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"run_id": run_id, "run_dir": str(run_dir), "formal_count": len(formal), "discovery_count": len(discovery), "challenger_unique_count": len(qa["challenger_unique"]), "dedup_count": len(combined)}
