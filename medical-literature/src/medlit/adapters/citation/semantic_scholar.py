from __future__ import annotations

import asyncio
import hashlib
import json
from typing import Any, Callable
from urllib.parse import quote
from urllib.request import Request, urlopen

from medlit.domain.models import CitationEdge


class SemanticScholarCitationAdapter:
    """S2 citation adapter; depth 1 is the safe default for snowballing."""

    base_url = "https://api.semanticscholar.org/graph/v1/paper"

    def __init__(self, request_json: Callable[[str], dict[str, Any]] | None = None, *, allow_deep: bool = False):
        self._request_json = request_json or self._request
        self.allow_deep = allow_deep

    @staticmethod
    def _request(url: str) -> dict[str, Any]:
        request = Request(url, headers={"Accept": "application/json", "User-Agent": "medlit/0.1"})
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

    @staticmethod
    def _external_id(paper_id: str) -> str:
        value = paper_id.strip()
        if value.startswith("doi:"):
            return f"DOI:{value[4:]}"
        if value.startswith("pmid:"):
            return f"PMID:{value[5:]}"
        if value.startswith("s2:"):
            return value[3:]
        return value

    @staticmethod
    def _canonical_id(item: dict[str, Any]) -> str:
        paper_id = item.get("paperId")
        if paper_id:
            return f"s2:{paper_id}"
        external = item.get("externalIds") or {}
        if external.get("DOI"):
            return f"doi:{external['DOI'].casefold()}"
        if external.get("PubMed"):
            return f"pmid:{external['PubMed']}"
        digest = hashlib.sha256(json.dumps(item, sort_keys=True).encode("utf-8")).hexdigest()[:20]
        return f"s2:unknown-{digest}"

    def _check_depth(self, depth: int) -> None:
        if depth < 1:
            raise ValueError("citation depth must be >= 1")
        if depth > 1 and not self.allow_deep:
            raise ValueError("depth > 1 requires explicit allow_deep=True")

    async def references(self, paper_id: str, *, depth: int = 1, run_id: str) -> list[CitationEdge]:
        self._check_depth(depth)
        url = f"{self.base_url}/{quote(self._external_id(paper_id), safe=':')}/references"
        payload = await asyncio.to_thread(self._request_json, url)
        source = paper_id if ":" in paper_id else f"s2:{paper_id}"
        return [
            CitationEdge(
                edge_id=f"edge:{hashlib.sha256((source + target + 'CITES').encode()).hexdigest()[:20]}",
                source_paper_id=source,
                target_paper_id=target,
                direction="CITES",
                provider="semantic-scholar",
                depth=depth,
                run_id=run_id,
            )
            for item in payload.get("data", [])
            if (target := self._canonical_id(item.get("citedPaper") or {}))
        ]

    async def citations(self, paper_id: str, *, depth: int = 1, run_id: str) -> list[CitationEdge]:
        self._check_depth(depth)
        url = f"{self.base_url}/{quote(self._external_id(paper_id), safe=':')}/citations"
        payload = await asyncio.to_thread(self._request_json, url)
        target = paper_id if ":" in paper_id else f"s2:{paper_id}"
        return [
            CitationEdge(
                edge_id=f"edge:{hashlib.sha256((source + target + 'CITED_BY').encode()).hexdigest()[:20]}",
                source_paper_id=source,
                target_paper_id=target,
                direction="CITED_BY",
                provider="semantic-scholar",
                depth=depth,
                run_id=run_id,
            )
            for item in payload.get("data", [])
            if (source := self._canonical_id(item.get("citingPaper") or {}))
        ]

    async def related(self, paper_id: str, *, run_id: str) -> list[CitationEdge]:
        url = f"{self.base_url}/{quote(self._external_id(paper_id), safe=':')}/recommendations"
        payload = await asyncio.to_thread(self._request_json, url)
        source = paper_id if ":" in paper_id else f"s2:{paper_id}"
        return [
            CitationEdge(
                edge_id=f"edge:{hashlib.sha256((source + target + 'RELATED').encode()).hexdigest()[:20]}",
                source_paper_id=source,
                target_paper_id=target,
                direction="RELATED",
                provider="semantic-scholar",
                depth=1,
                run_id=run_id,
            )
            for item in payload.get("recommendedPapers", payload.get("data", []))
            if (target := self._canonical_id(item))
        ]
