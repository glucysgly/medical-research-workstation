from __future__ import annotations

import asyncio
import json
from typing import Any, Callable
from urllib.parse import quote
from urllib.request import Request, urlopen

from medlit.canonical.normalize import normalize_paper
from medlit.domain.models import CanonicalPaper, SourceRole


class PubMedEutilsAdapter:
    """Thin official NCBI E-utilities fallback; it does not replace PubMed MCP."""

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self, *, email: str | None, api_key: str | None = None, request_json: Callable[[str], dict[str, Any]] | None = None):
        if not email or "@" not in email:
            raise ValueError("NCBI email is required for the official PubMed fallback")
        self.email = email
        self.api_key = api_key
        self._request_json = request_json or self._request

    @staticmethod
    def _request(url: str) -> dict[str, Any]:
        request = Request(url, headers={"Accept": "application/json", "User-Agent": "medlit/0.1"})
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

    async def search(self, query: str, *, run_id: str, retmax: int = 100) -> list[CanonicalPaper]:
        common = f"&email={quote(self.email)}&tool=medlit"
        if self.api_key:
            common += f"&api_key={quote(self.api_key)}"
        search_url = f"{self.base_url}/esearch.fcgi?db=pubmed&term={quote(query)}&retmode=json&retmax={min(retmax, 10000)}{common}"
        search_payload = await asyncio.to_thread(self._request_json, search_url)
        ids = search_payload.get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []
        summary_url = f"{self.base_url}/esummary.fcgi?db=pubmed&id={','.join(map(str, ids))}&retmode=json{common}"
        summary_payload = await asyncio.to_thread(self._request_json, summary_url)
        result = summary_payload.get("result", {})
        papers: list[CanonicalPaper] = []
        for pmid in ids:
            raw = dict(result.get(str(pmid), {}))
            raw["pmid"] = str(pmid)
            article_ids = {item.get("idtype"): item.get("value") for item in raw.get("articleids", []) if isinstance(item, dict)}
            raw["doi"] = article_ids.get("doi")
            raw["pmcid"] = article_ids.get("pmc")
            raw["authors"] = raw.get("authors", [])
            papers.append(normalize_paper(raw, source="pubmed", source_role=SourceRole.FORMAL_DATABASE, run_id=run_id, query=query))
        return papers
