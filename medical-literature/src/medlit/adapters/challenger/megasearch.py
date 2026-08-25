from __future__ import annotations

from typing import Any, Callable


class ChallengerAdapter:
    """Thin wrapper around scholar-megasearch; failure never fails formal search."""

    def __init__(self, search_fn: Callable[[str], list[dict[str, Any]]] | None = None):
        self._search_fn = search_fn

    def search(self, query: str) -> dict[str, Any]:
        if self._search_fn is None:
            return {"status": "SKIP", "records": [], "warning": "scholar-megasearch is not configured"}
        try:
            records = self._search_fn(query)
            return {"status": "READY", "records": list(records), "warning": None}
        except Exception as exc:  # deliberate degradation boundary for optional challenger
            return {"status": "DEGRADED", "records": [], "warning": str(exc)}
