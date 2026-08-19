from __future__ import annotations

import re
from typing import Any, Iterable

from medlit.canonical.normalize import normalize_doi, normalize_text


def lint_query(query: str, *, database: str) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    if query.count("(") != query.count(")"):
        issues.append({"code": "UNMATCHED_PARENTHESES", "severity": "ERROR", "detail": "parentheses are not balanced"})
    if query.count('"') % 2:
        issues.append({"code": "UNTERMINATED_PHRASE", "severity": "ERROR", "detail": "quoted phrase is not closed"})
    if re.search(r"\b(?:AND|OR|NOT)\s+(?:AND|OR|NOT)\b", query, flags=re.I):
        issues.append({"code": "INVALID_BOOLEAN", "severity": "ERROR", "detail": "boolean operators are adjacent"})
    if re.search(r"\d{4}:\d{4}\[(?:dp|pdat|crdt)\]", query, flags=re.I):
        issues.append({"code": "ACCIDENTAL_DATE_LIMIT", "severity": "WARN", "detail": f"date restriction detected for {database}"})
    if re.search(r"\bNOT\b", query, flags=re.I):
        issues.append({"code": "NOT_REVIEW", "severity": "WARN", "detail": "NOT can remove eligible records and requires review"})
    terms = re.findall(r"[A-Za-z][A-Za-z-]+", query.casefold())
    duplicate_terms = sorted({term for term in terms if terms.count(term) > 1})
    if duplicate_terms:
        issues.append({"code": "DUPLICATE_SYNONYM", "severity": "INFO", "detail": ", ".join(duplicate_terms)})
    return {"database": database, "query": query, "issues": issues, "status": "FAIL" if any(i["severity"] == "ERROR" for i in issues) else "PASS"}


def _record_identifiers(record: Any) -> set[str]:
    if hasattr(record, "doi"):
        values = [getattr(record, "doi", None), getattr(record, "pmid", None), getattr(record, "pmcid", None), getattr(record, "title", None)]
    else:
        values = [record.get("doi"), record.get("pmid"), record.get("pmcid"), record.get("title")]
    identifiers: set[str] = set()
    for value in values:
        if value in (None, ""):
            continue
        text = normalize_doi(value) if str(value).lower().startswith(("10.", "http")) else normalize_text(value)
        identifiers.add(text)
    return identifiers


def known_item_recall(known_items: Iterable[dict[str, Any]], returned_records: Iterable[Any]) -> dict[str, Any]:
    known_items = list(known_items)
    returned = set().union(*(_record_identifiers(record) for record in returned_records)) if returned_records else set()
    required: list[str] = []
    found: list[str] = []
    missing_mandatory: list[str] = []
    for item in known_items:
        raw_id = str(item.get("id") or item.get("doi") or item.get("pmid") or item.get("title") or "")
        normalized = normalize_doi(raw_id) if raw_id.startswith(("10.", "http")) else normalize_text(raw_id)
        if item.get("mandatory", True):
            required.append(raw_id)
        if normalized in returned:
            found.append(raw_id)
        elif item.get("mandatory", True):
            missing_mandatory.append(raw_id)
    recall = len(found) / max(1, len(known_items))
    return {"known_item_count": len(required), "found": found, "missing_mandatory": missing_mandatory, "recall": recall, "status": "PASS" if not missing_mandatory else "SEARCH_STRATEGY_FAIL"}
