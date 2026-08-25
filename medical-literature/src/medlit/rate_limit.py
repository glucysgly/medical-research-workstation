from __future__ import annotations

from copy import deepcopy
from typing import Any


DEFAULT_POLICY = {"concurrency": 1, "requests_per_second": 1.0, "retry_after": 1.0, "backoff": 2.0, "max_retries": 0}


class RateLimitManager:
    def __init__(self, policies: dict[str, dict[str, Any]] | None = None):
        self._policies = {key: {**DEFAULT_POLICY, **value} for key, value in (policies or {}).items()}

    def policy(self, provider: str) -> dict[str, Any]:
        return deepcopy(self._policies.get(provider, {**DEFAULT_POLICY, "max_retries": 0}))
