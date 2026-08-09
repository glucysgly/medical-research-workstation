#!/usr/bin/env python3
"""Audit a public candidate without printing matched sensitive text."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


TEXT_SUFFIXES = {".md", ".txt", ".py", ".ps1", ".cmd", ".bat", ".yml", ".yaml", ".json", ".toml", ".csv", ".tsv", ".cff", ".sh", ".cff"}
SKIP_PARTS = {".git", "__pycache__", ".venv", "cache", "logs", "backups", "dist"}
SKIP_FILES = {"public_release_audit.py"}
PRIVATE_PATH_RE = re.compile(r"(?i)(?:[a-z]:\\users\\[^\s`'\"<>]+|/home/[^\s`'\"<>]+|/mnt/[cd]/users/[^\s`'\"<>]+)")
SECRET_RE = re.compile(
    r"(?i)(?:sk-[A-Za-z0-9]{20,}|gh[pous]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [^-]+-----|"
    r"(?:api[_-]?key|access[_-]?token|password|passwd|secret|cookie|authorization)\s*[:=]\s*[^\s,;]{12,})"
)
PHI_HEADER_RE = re.compile(r"(?i)^\s*(?:patient_id|medical_record_number|mrn|身份证号|姓名)\s*[,=:]")


def files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or path.name in SKIP_FILES or any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def scan(root: Path) -> dict:
    findings = {"private_path": [], "secret": [], "phi_pii": []}
    scanned = 0
    for path in files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        scanned += 1
        relative = path.relative_to(root).as_posix()
        for number, line in enumerate(text.splitlines(), 1):
            if PRIVATE_PATH_RE.search(line):
                findings["private_path"].append({"path": relative, "line": number})
            if SECRET_RE.search(line):
                findings["secret"].append({"path": relative, "line": number})
            if PHI_HEADER_RE.search(line):
                findings["phi_pii"].append({"path": relative, "line": number})
    try:
        history_count = int(subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=root, text=True).strip())
    except (OSError, ValueError, subprocess.CalledProcessError):
        history_count = None
    counts = {key: len(value) for key, value in findings.items()}
    return {
        "schema_version": 1,
        "status": "PASS" if not any(counts.values()) else "FAIL",
        "files_scanned": scanned,
        "history_refs_scanned": history_count,
        "private_path_matches": counts["private_path"],
        "secret_matches": counts["secret"],
        "phi_pii_matches": counts["phi_pii"],
        "findings": findings,
        "license_unknown": "manual_inventory_required",
        "sensitive_values_emitted": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a public release tree")
    parser.add_argument("--root", default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve() if args.root else Path(__file__).resolve().parents[1]
    result = scan(root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(f"public release audit: {result['status']}")
        print(f"files_scanned: {result['files_scanned']}")
        print(f"private_path_matches: {result['private_path_matches']}")
        print(f"secret_matches: {result['secret_matches']}")
        print(f"phi_pii_matches: {result['phi_pii_matches']}")
    return 1 if args.strict and result["status"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
