from __future__ import annotations

import asyncio
from difflib import SequenceMatcher
from typing import Any, Callable

from medlit.canonical.normalize import normalize_doi, normalize_text
from medlit.domain.models import VerificationResult


AUTHORITATIVE = {"crossref", "pubmed", "publisher", "doi-resolver"}


def _title_score(left: str | None, right: str | None) -> float:
    return SequenceMatcher(None, normalize_text(left), normalize_text(right)).ratio()


def evaluate_verification(
    *,
    title: str,
    doi: str | None,
    year: int | None,
    authors: list[str],
    provider_records: dict[str, dict[str, Any]],
) -> VerificationResult:
    supplied_doi = normalize_doi(doi)
    matched: list[str] = []
    reasons: list[str] = []
    for provider, record in provider_records.items():
        record_doi = normalize_doi(record.get("doi"))
        score = _title_score(title, record.get("title"))
        year_ok = year is None or record.get("year") in (None, year, year - 1, year + 1)
        if supplied_doi and record_doi and supplied_doi == record_doi and score >= 0.85 and year_ok:
            matched.append(provider)
        elif supplied_doi and record_doi and supplied_doi != record_doi:
            reasons.append(f"{provider}: DOI mismatch")
        elif score < 0.85:
            reasons.append(f"{provider}: title mismatch")
    authoritative = [provider for provider in matched if provider in AUTHORITATIVE]
    if supplied_doi and len(authoritative) >= 2:
        state = "VERIFIED_HIGH"
    elif reasons and supplied_doi and not matched:
        state = "CONFLICT"
    elif matched:
        state = "VERIFIED_MEDIUM"
    elif not provider_records:
        state = "UNVERIFIED"
        reasons.append("no provider response")
    else:
        state = "UNVERIFIED"
    return VerificationResult(state=state, reasons=reasons, matched_providers=matched, provider_records=provider_records)


class FallbackCitationVerifier:
    """Crossref + PubMed fallback for the optional doi-mcp verifier."""

    def __init__(self, lookup: Callable[[str, dict[str, Any]], dict[str, Any] | None] | None = None):
        self._lookup = lookup

    async def verify_citation(
        self,
        title: str,
        doi: str | None,
        pmid: str | None,
        authors: list[str],
        year: int | None,
    ) -> VerificationResult:
        if self._lookup is None:
            return VerificationResult(state="UNVERIFIED", reasons=["fallback lookup is not configured"])
        query = {"title": title, "doi": doi, "pmid": pmid, "authors": authors, "year": year}
        records: dict[str, dict[str, Any]] = {}
        for provider in ("crossref", "pubmed"):
            record = await asyncio.to_thread(self._lookup, provider, query)
            if record:
                records[provider] = record
        return evaluate_verification(title=title, doi=doi, year=year, authors=authors, provider_records=records)
