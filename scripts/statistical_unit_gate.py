#!/usr/bin/env python3
"""Small protected-core gate for donor-aware single-cell inference."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Mapping


def validate_donor_unit(rows: Iterable[Mapping[str, object]], *, unit: str = "donor") -> dict[str, object]:
    if unit != "donor":
        raise ValueError("single-cell biological inference requires donor as the inferential unit")
    donor_groups: dict[tuple[str, str], set[str]] = defaultdict(set)
    row_count = 0
    for row in rows:
        donor = str(row.get("donor_id", "")).strip()
        group = str(row.get("group", "")).strip()
        if not donor or not group:
            raise ValueError("donor_id and group are required for donor-aware inference")
        donor_groups[(group, donor)].add(str(row.get("cell_id", row_count)))
        row_count += 1
    by_group: dict[str, int] = defaultdict(int)
    for group, _donor in donor_groups:
        by_group[group] += 1
    return {
        "inferential_unit": "donor",
        "cell_rows_seen": row_count,
        "donors_by_group": dict(sorted(by_group.items())),
        "cell_level_independence": False,
        "status": "PASS",
    }
