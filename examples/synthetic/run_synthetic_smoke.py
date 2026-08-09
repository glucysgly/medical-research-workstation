#!/usr/bin/env python3
"""Run the smallest public, synthetic-only workflow."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    fixture_root = root / "tests" / "fixtures" / "synthetic"
    csv_files = sorted(fixture_root.glob("*.csv"))
    rows = {}
    for path in csv_files:
        with path.open(encoding="utf-8", newline="") as handle:
            table = list(csv.reader(handle))
        if len(table) < 2 or not table[0]:
            raise SystemExit(f"invalid synthetic fixture: {path.name}")
        rows[path.name] = {"columns": len(table[0]), "rows": len(table) - 1}
    route = subprocess.check_output(
        [sys.executable, str(root / "scripts" / "researchctl.py"), "route", "分析这批 qPCR 数据", "--json"],
        cwd=root,
        text=True,
    )
    route_record = json.loads(route)
    if route_record.get("workflow_key") != "qpcr":
        raise SystemExit("synthetic route did not select qpcr")
    print(json.dumps({"status": "PASS", "synthetic_only": True, "fixtures": rows, "route": "qpcr"}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
