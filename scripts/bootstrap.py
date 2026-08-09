#!/usr/bin/env python3
"""Bounded, non-installing bootstrap for a local research workbench."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


DIRECTORIES = ("projects", "logs", "cache", "evolution", "dist")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create only local workbench directories")
    parser.add_argument("--root", default=os.environ.get("RESEARCHCTL_ROOT"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve() if args.root else Path(__file__).resolve().parents[1]
    targets = [root / item for item in DIRECTORIES]
    created = []
    existing = []
    if not args.dry_run:
        for target in targets:
            if target.exists():
                existing.append(target.relative_to(root).as_posix())
            else:
                target.mkdir(parents=True, exist_ok=True)
                created.append(target.relative_to(root).as_posix())
    result = {
        "ok": True,
        "command": "bootstrap",
        "mode": "dry_run" if args.dry_run else "local_directories_only",
        "root": "<resolved-local-root>",
        "requested_directories": list(DIRECTORIES),
        "created": created,
        "already_present": existing,
        "installations": [],
        "uploads": [],
        "overwrites": [],
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(f"bootstrap: PASS ({result['mode']})")
        print(f"directories: {len(DIRECTORIES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
