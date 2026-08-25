"""Read the repository's pinned upstream inventory without network access."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def _parse_lock(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError(f"upstream lock file does not exist: {path}")
    section: str | None = None
    current: dict[str, Any] | None = None
    providers: list[dict[str, Any]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if not raw_line.startswith(" ") and line.endswith(":"):
            section = line[:-1]
            current = None
            continue
        match = re.match(r"^  ([A-Za-z0-9_-]+):$", raw_line)
        if match and section in {"upstreams", "optional"}:
            current = {"name": match.group(1), "section": section}
            providers.append(current)
            continue
        if current is None or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.lower() in {"true", "false"}:
            parsed: Any = value.lower() == "true"
        else:
            parsed = value.strip('"\'')
        current[key.strip()] = parsed
    return providers


def check_locked_upstreams(lock_path: str | Path) -> dict[str, Any]:
    """Return lock metadata and explicitly avoid presenting it as a live audit."""

    providers = []
    for provider in _parse_lock(Path(lock_path)):
        providers.append(
            {
                "name": provider.get("name"),
                "section": provider.get("section"),
                "repo": provider.get("repo"),
                "locked_sha": provider.get("commit"),
                "license": provider.get("license"),
                "tier": provider.get("tier"),
                "verified": provider.get("verified", False),
                "latest_sha": None,
                "latest_release": None,
                "breaking_change_risk": "UNKNOWN",
                "tests": "NOT_RUN",
                "recommendation": "run isolated audit before promotion",
            }
        )
    return {"status": "LOCKED_UNVERIFIED", "source": str(lock_path), "network_probe": "NOT_RUN", "providers": providers}
