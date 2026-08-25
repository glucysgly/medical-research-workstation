from __future__ import annotations

import json
from typing import Any


FRAMEWORKS = {"PICO", "PECO", "PCC", "SPIDER", "PIRD", "PICOTS"}


def build_query_artifact(*, question: str, review_type: str, framework: str, concepts: list[dict[str, Any]], databases: list[str], queries: dict[str, str], trial_queries: dict[str, str | None] | None = None, date_limits: Any = None, language_limits: Any = None, study_design_filters: list[str] | None = None, peer_review: dict[str, Any] | None = None) -> dict[str, Any]:
    normalized_framework = framework.upper()
    if normalized_framework not in FRAMEWORKS:
        raise ValueError(f"framework must be one of {sorted(FRAMEWORKS)}")
    missing = [database for database in databases if database not in queries]
    if missing:
        raise ValueError(f"missing database-specific queries: {', '.join(missing)}")
    return {
        "question": question,
        "review_type": review_type,
        "framework": normalized_framework,
        "concepts": concepts,
        "databases": databases,
        "queries": queries,
        "trial_queries": trial_queries or {},
        "date_limits": date_limits,
        "language_limits": language_limits,
        "study_design_filters": study_design_filters or [],
        "peer_review": peer_review or {"status": "DRAFT", "reviewer": None, "notes": None},
    }


def _scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str) and value and all(char.isalnum() or char in "._-/" for char in value):
        return value
    return json.dumps(value, ensure_ascii=False)


def render_yaml(value: Any, indent: int = 0) -> str:
    spaces = " " * indent
    lines: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if isinstance(child, (dict, list)):
                lines.append(f"{spaces}{key}:")
                lines.append(render_yaml(child, indent + 2).rstrip("\n"))
            else:
                lines.append(f"{spaces}{key}: {_scalar(child)}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                lines.append(f"{spaces}-")
                lines.append(render_yaml(item, indent + 2).rstrip("\n"))
            else:
                lines.append(f"{spaces}- {_scalar(item)}")
    else:
        lines.append(f"{spaces}{_scalar(value)}")
    return "\n".join(lines) + "\n"
