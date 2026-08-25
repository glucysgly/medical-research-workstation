from __future__ import annotations

from typing import Any, Iterable

from medlit.domain.models import CanonicalPaper


def _ids(records: Iterable[CanonicalPaper]) -> set[str]:
    return {record.paper_id for record in records}


def compare_formal_challenger(formal: Iterable[CanonicalPaper], challenger: Iterable[CanonicalPaper]) -> dict[str, Any]:
    formal_ids = _ids(formal)
    challenger_ids = _ids(challenger)
    unique = sorted(challenger_ids - formal_ids)
    return {
        "formal_count": len(formal_ids),
        "challenger_count": len(challenger_ids),
        "intersection": len(formal_ids & challenger_ids),
        "formal_unique": sorted(formal_ids - challenger_ids),
        "challenger_unique": unique,
        "challenger_unique_verified": [],
        "challenger_unique_relevant": [],
        "coverage_warnings": ["challenger_unique requires manual gap classification"] if unique else [],
    }


def source_overlap_matrix(corpora: dict[str, Iterable[CanonicalPaper]]) -> dict[str, Any]:
    ids = {name: _ids(records) for name, records in corpora.items()}
    names = list(ids)
    rows: dict[str, dict[str, int]] = {}
    for left in names:
        rows[left] = {right: len(ids[left] & ids[right]) for right in names}
    return {"sources": names, "rows": rows}


def classify_gap(*, reason: str | None = None, title: str | None = None) -> str:
    if reason:
        return reason
    if title and "preprint" in title.casefold():
        return "PREPRINT_ONLY"
    return "OTHER"
