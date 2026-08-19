from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import replace
from typing import Any, Iterable

from medlit.domain.models import CanonicalPaper, SourceRole


def normalize_text(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def normalize_doi(value: Any) -> str | None:
    if not value:
        return None
    doi = str(value).strip()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.I)
    doi = doi.strip().rstrip(".,;:)").casefold()
    return doi or None


def normalize_identifier(value: Any, prefix: str) -> str | None:
    if not value:
        return None
    text = str(value).strip()
    text = re.sub(rf"^{prefix}:?", "", text, flags=re.I)
    return text or None


def _list_values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return [str(item) for item in value if item not in (None, "")]


def _authors(value: Any) -> list[str]:
    output: list[str] = []
    for author in value or []:
        if isinstance(author, str):
            name = author
        elif isinstance(author, dict):
            name = author.get("name") or " ".join(filter(None, [author.get("given"), author.get("family")]))
        else:
            name = str(author)
        if name and name not in output:
            output.append(name)
    return output


def _year(value: Any) -> int | None:
    if value in (None, ""):
        return None
    match = re.search(r"\b(19|20)\d{2}\b", str(value))
    return int(match.group(0)) if match else None


def _paper_id(doi: str | None, pmid: str | None, pmcid: str | None, title: str) -> str:
    if doi:
        return f"doi:{doi}"
    if pmid:
        return f"pmid:{pmid}"
    if pmcid:
        return f"pmcid:{pmcid}"
    digest = hashlib.sha256(normalize_text(title).encode("utf-8")).hexdigest()[:20]
    return f"title:{digest}"


def normalize_paper(
    raw: dict[str, Any],
    *,
    source: str,
    source_role: SourceRole | str,
    run_id: str,
    query: str | None = None,
    raw_payload_path: str | None = None,
) -> CanonicalPaper:
    title = str(raw.get("title") or raw.get("articleTitle") or raw.get("name") or "").strip()
    doi = normalize_doi(raw.get("doi") or raw.get("DOI"))
    pmid = normalize_identifier(raw.get("pmid") or raw.get("PMID"), "pmid")
    pmcid = normalize_identifier(raw.get("pmcid") or raw.get("PMCID"), "pmc")
    role = source_role.value if isinstance(source_role, SourceRole) else str(source_role)
    source_record = {
        "source": source,
        "source_role": role,
        "query": query,
        "query_hash": hashlib.sha256((query or "").encode("utf-8")).hexdigest(),
        "run_id": run_id,
        "retrieved_at": raw.get("retrieved_at"),
        "raw_identifier": doi or pmid or pmcid or title,
        "raw_payload_path": raw_payload_path,
    }
    return CanonicalPaper(
        paper_id=_paper_id(doi, pmid, pmcid, title),
        title=title,
        abstract=raw.get("abstract") or raw.get("summary"),
        authors=_authors(raw.get("authors") or raw.get("author")),
        year=_year(raw.get("year") or raw.get("publication_year") or raw.get("date")),
        journal=raw.get("journal") or raw.get("venue"),
        doi=doi,
        pmid=pmid,
        pmcid=pmcid,
        issn=_list_values(raw.get("issn")),
        publication_types=_list_values(raw.get("publication_types") or raw.get("publicationType")),
        mesh_terms=_list_values(raw.get("mesh_terms") or raw.get("meshTerms")),
        keywords=_list_values(raw.get("keywords")),
        language=raw.get("language"),
        source_urls=_list_values(raw.get("source_urls") or raw.get("urls") or raw.get("url")),
        oa_status=raw.get("oa_status"),
        raw_sources=[source_record],
        discovery_methods=[source],
        source_roles=[role],
        first_discovered_run_id=run_id,
        verification_status=str(raw.get("verification_status") or "UNVERIFIED"),
    )


def _merge_unique(left: list[str], right: Iterable[str]) -> list[str]:
    result = list(left)
    for value in right:
        if value and value not in result:
            result.append(value)
    return result


def _merge(left: CanonicalPaper, right: CanonicalPaper) -> CanonicalPaper:
    paper = replace(left)
    for field in ("title", "abstract", "journal", "language", "oa_status", "first_discovered_run_id"):
        if not getattr(paper, field) and getattr(right, field):
            setattr(paper, field, getattr(right, field))
    for field in ("authors", "issn", "publication_types", "mesh_terms", "keywords", "source_urls", "discovery_methods", "source_roles", "raw_sources"):
        setattr(paper, field, _merge_unique(getattr(paper, field), getattr(right, field)))
    for field in ("doi", "pmid", "pmcid", "year"):
        if not getattr(paper, field) and getattr(right, field):
            setattr(paper, field, getattr(right, field))
    if paper.verification_status == "UNVERIFIED" and right.verification_status != "UNVERIFIED":
        paper.verification_status = right.verification_status
    return paper


def _match(left: CanonicalPaper, right: CanonicalPaper) -> str | None:
    if left.doi and right.doi and left.doi == right.doi:
        return "doi_exact"
    if left.pmid and right.pmid and left.pmid == right.pmid:
        return "pmid_exact"
    if left.pmcid and right.pmcid and left.pmcid == right.pmcid:
        return "pmcid_exact"
    if left.title and right.title and normalize_text(left.title) == normalize_text(right.title):
        return "normalized_title_exact"
    return None


def deduplicate_papers(papers: Iterable[CanonicalPaper]) -> tuple[list[CanonicalPaper], list[dict[str, Any]]]:
    unique: list[CanonicalPaper] = []
    audit: list[dict[str, Any]] = []
    for paper in papers:
        match_index = None
        rule = None
        for index, existing in enumerate(unique):
            rule = _match(existing, paper)
            if rule:
                match_index = index
                break
        if match_index is None:
            unique.append(paper)
            continue
        existing = unique[match_index]
        unique[match_index] = _merge(existing, paper)
        audit.append({"kept_paper_id": existing.paper_id, "merged_paper_id": paper.paper_id, "match_rule": rule})
    return unique, audit
