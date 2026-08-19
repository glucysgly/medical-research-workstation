from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SourceRole(str, Enum):
    FORMAL_DATABASE = "FORMAL_DATABASE"
    DISCOVERY_ENGINE = "DISCOVERY_ENGINE"
    TRIAL_REGISTRY = "TRIAL_REGISTRY"
    CITATION_FORWARD = "CITATION_FORWARD"
    CITATION_BACKWARD = "CITATION_BACKWARD"
    CHALLENGER = "CHALLENGER"
    VERIFIER = "VERIFIER"
    LOCAL_LIBRARY = "LOCAL_LIBRARY"
    MANUAL_IMPORT = "MANUAL_IMPORT"


@dataclass
class CanonicalPaper:
    paper_id: str
    title: str
    abstract: str | None = None
    authors: list[str] = field(default_factory=list)
    year: int | None = None
    journal: str | None = None
    doi: str | None = None
    pmid: str | None = None
    pmcid: str | None = None
    issn: list[str] = field(default_factory=list)
    publication_types: list[str] = field(default_factory=list)
    mesh_terms: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    language: str | None = None
    source_urls: list[str] = field(default_factory=list)
    oa_status: str | None = None
    raw_sources: list[dict[str, Any]] = field(default_factory=list)
    discovery_methods: list[str] = field(default_factory=list)
    source_roles: list[str] = field(default_factory=list)
    first_discovered_run_id: str | None = None
    verification_status: str = "UNVERIFIED"

    def to_dict(self) -> dict[str, Any]:
        return {
            "paper_id": self.paper_id,
            "title": self.title,
            "abstract": self.abstract,
            "authors": self.authors,
            "year": self.year,
            "journal": self.journal,
            "doi": self.doi,
            "pmid": self.pmid,
            "pmcid": self.pmcid,
            "issn": self.issn,
            "publication_types": self.publication_types,
            "mesh_terms": self.mesh_terms,
            "keywords": self.keywords,
            "language": self.language,
            "source_urls": self.source_urls,
            "oa_status": self.oa_status,
            "raw_sources": self.raw_sources,
            "discovery_methods": self.discovery_methods,
            "source_roles": self.source_roles,
            "first_discovered_run_id": self.first_discovered_run_id,
            "verification_status": self.verification_status,
        }


@dataclass
class ClinicalTrial:
    trial_id: str
    registry: str
    title: str
    brief_summary: str | None = None
    status: str | None = None
    study_type: str | None = None
    phase: list[str] = field(default_factory=list)
    enrollment: int | None = None
    conditions: list[str] = field(default_factory=list)
    interventions: list[str] = field(default_factory=list)
    comparators: list[str] = field(default_factory=list)
    primary_outcomes: list[str] = field(default_factory=list)
    secondary_outcomes: list[str] = field(default_factory=list)
    eligibility: str | None = None
    sponsor: str | None = None
    collaborators: list[str] = field(default_factory=list)
    locations: list[str] = field(default_factory=list)
    start_date: str | None = None
    primary_completion_date: str | None = None
    completion_date: str | None = None
    results_posted: bool | None = None
    linked_publications: list[str] = field(default_factory=list)
    raw_source: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class CitationEdge:
    edge_id: str
    source_paper_id: str
    target_paper_id: str
    direction: str
    provider: str
    depth: int
    run_id: str

    def __post_init__(self) -> None:
        if self.depth < 1:
            raise ValueError("citation depth must be >= 1")
        if self.direction not in {"CITES", "CITED_BY", "RELATED"}:
            raise ValueError("citation direction must be CITES, CITED_BY or RELATED")


@dataclass
class VerificationResult:
    state: str
    reasons: list[str] = field(default_factory=list)
    matched_providers: list[str] = field(default_factory=list)
    provider_records: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()
