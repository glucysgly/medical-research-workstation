"""Dependency-free static check for the synthetic v5 demo."""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "synthetic_outcomes.csv"
REQUIRED = {"sample_id", "arm", "baseline_units", "followup_units", "change_units"}


def check() -> dict[str, float | int | str]:
    rows = list(csv.DictReader(RAW.open(newline="", encoding="utf-8")))
    if not rows:
        raise ValueError("synthetic input is empty")
    if not REQUIRED.issubset(rows[0]):
        raise ValueError("required columns are missing")
    if len({row["sample_id"] for row in rows}) != len(rows):
        raise ValueError("sample_id must be unique")
    means = {}
    for arm in {row["arm"] for row in rows}:
        values = [float(row["change_units"]) for row in rows if row["arm"] == arm]
        means[arm] = sum(values) / len(values)
    return {"rows": len(rows), "control_mean": means["control"], "treatment_mean": means["treatment"], "effect": means["treatment"] - means["control"], "unit": "synthetic_participant"}


if __name__ == "__main__":
    print(check())
