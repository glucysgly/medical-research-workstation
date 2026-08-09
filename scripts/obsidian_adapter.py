#!/usr/bin/env python3
"""Read-only, local-filesystem-first Obsidian vault search adapter."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


SECRET_KEY = re.compile(r"(?i)(api[_-]?key|access[_-]?token|password|passwd|secret|cookie|authorization|^token$)")
SECRET_VALUE = re.compile(r"(?is)(?:api[_-]?key|access[_-]?token|password|passwd|secret|cookie|authorization)\s*[:=]\s*[^\s,;]+")


class AdapterError(Exception):
    """Expected, user-facing adapter error."""


def _resolve_vault(value: str | None) -> Path | None:
    configured = value or os.environ.get("OBSIDIAN_VAULT")
    if not configured:
        return None
    if "\x00" in configured:
        raise AdapterError("vault path contains a NUL byte")
    root = Path(configured).expanduser().resolve(strict=False)
    return root


def _inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def _relative_target(root: Path, requested: str | None, *, directory: bool = False) -> Path:
    if not requested:
        return root
    relative = Path(requested)
    if any(part == ".." for part in relative.parts):
        raise AdapterError("path outside vault is not allowed")
    candidate = relative if relative.is_absolute() else root / relative
    resolved = candidate.resolve(strict=False)
    if not _inside(root, resolved):
        raise AdapterError("path outside vault is not allowed")
    if directory and resolved.exists() and not resolved.is_dir():
        raise AdapterError("search path must be a directory")
    return resolved


def _redact(text: str) -> str:
    if SECRET_VALUE.search(text):
        return "[REDACTED]"
    return text


def _title(lines: list[str], path: Path) -> str:
    for line in lines[:80]:
        match = re.match(r"^\s*#\s+(.+?)\s*$", line)
        if match:
            return _redact(match.group(1))[:200]
    return path.stem


def _matches(path: Path, query: str) -> list[dict[str, Any]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return []
    lines = text.splitlines()
    needle = query.casefold()
    return [{"line": number, "summary": _redact(line.strip())[:240]} for number, line in enumerate(lines, 1) if needle in line.casefold()]


def search_vault(root: Path, query: str, relative_path: str | None = None) -> dict[str, Any]:
    if not query.strip():
        raise AdapterError("search query must not be empty")
    base = _relative_target(root, relative_path, directory=True)
    if not root.is_dir():
        return {"ok": True, "command": "search", "status": "not_configured", "count": 0, "results": []}
    if not base.exists():
        return {"ok": True, "command": "search", "status": "ok", "count": 0, "results": []}
    files = [base] if base.is_file() else sorted(base.rglob("*.md"), key=lambda item: item.as_posix().casefold())
    results = []
    for path in files:
        resolved = path.resolve(strict=False)
        if not path.is_file() or path.is_symlink() or not _inside(root, resolved):
            continue
        matches = _matches(path, query)
        if matches:
            try:
                relative = path.relative_to(root).as_posix()
            except ValueError:
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeError):
                continue
            results.append({"path": relative, "title": _title(lines, path), "matches": matches})
    return {"ok": True, "command": "search", "status": "ok", "count": len(results), "results": results}


def execute(args: argparse.Namespace) -> dict[str, Any]:
    root = _resolve_vault(args.vault)
    if root is None:
        return {"ok": True, "command": args.command, "status": "not_configured", "configured": False, "path": "."}
    if args.command == "health":
        return {"ok": True, "command": "health", "status": "configured" if root.is_dir() else "not_configured", "configured": root.is_dir(), "path": "."}
    return search_vault(root, args.query, args.path)


def _scrub(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): ("[REDACTED]" if SECRET_KEY.search(str(key)) else _scrub(item)) for key, item in value.items()}
    if isinstance(value, list):
        return [_scrub(item) for item in value]
    if isinstance(value, str) and SECRET_VALUE.search(value):
        return "[REDACTED]"
    return value


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only Obsidian vault adapter")
    sub = parser.add_subparsers(dest="command", required=True)
    health = sub.add_parser("health")
    health.add_argument("--vault")
    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--vault")
    search.add_argument("--path")
    return parser


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in raw or "-j" in raw
    raw = [item for item in raw if item not in {"--json", "-j"}]
    try:
        result = execute(make_parser().parse_args(raw))
    except (AdapterError, OSError, ValueError) as exc:
        result = {"ok": False, "status": "error", "error": str(exc)}
    if as_json:
        print(json.dumps(_scrub(result), ensure_ascii=False, sort_keys=True))
    elif result.get("ok"):
        print(f"{result.get('command', 'obsidian')}: {result.get('status', 'ok')}")
    else:
        print(f"ERROR: {result.get('error', 'failed')}", file=sys.stderr)
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
