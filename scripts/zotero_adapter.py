#!/usr/bin/env python3
"""Read-only, standard-library Zotero metadata adapter.

The adapter intentionally reads a JSON export supplied by the caller.  It
does not connect to Zotero, write to a library, or emit attachments/full text.
"""

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
METADATA_KEYS = (
    "key",
    "itemType",
    "title",
    "creators",
    "date",
    "DOI",
    "publicationTitle",
    "journalAbbreviation",
    "volume",
    "issue",
    "pages",
    "publisher",
    "place",
    "url",
    "language",
    "version",
)


class AdapterError(Exception):
    """Expected, user-facing adapter error."""


def _safe_path(value: str | os.PathLike[str], *, must_exist: bool = False) -> Path:
    raw = os.fspath(value)
    if "\x00" in raw:
        raise AdapterError("path contains a NUL byte")
    path = Path(raw).expanduser()
    resolved = path.resolve(strict=False)
    if must_exist and not resolved.is_file():
        raise AdapterError("library path is not a readable file")
    return resolved


def default_library_path() -> Path:
    configured = os.environ.get("ZOTERO_LIBRARY_JSON")
    if configured:
        return _safe_path(configured)
    candidates = [
        Path.cwd() / "zotero-library.json",
        Path(os.environ.get("APPDATA", "")) / "Zotero" / "library.json",
        Path.home() / ".zotero" / "library.json",
    ]
    return next((path.resolve() for path in candidates if path.is_file()), candidates[0].resolve())


def library_path(explicit: str | None) -> Path:
    return _safe_path(explicit) if explicit else default_library_path()


def _load_items(path: Path) -> list[dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8-sig") as handle:
            payload = json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AdapterError(f"unable to read library JSON: {type(exc).__name__}") from exc
    if isinstance(payload, dict):
        raw_items = payload.get("items", payload.get("library", []))
    else:
        raw_items = payload
    if not isinstance(raw_items, list):
        raise AdapterError("library JSON must contain an items list")
    return [item for item in raw_items if isinstance(item, dict)]


def _item_data(item: dict[str, Any]) -> dict[str, Any]:
    nested = item.get("data")
    return nested if isinstance(nested, dict) else item


def _creator_metadata(creators: Any) -> list[dict[str, str]]:
    if not isinstance(creators, list):
        return []
    result = []
    for creator in creators:
        if not isinstance(creator, dict):
            continue
        selected = {}
        for key in ("creatorType", "firstName", "lastName", "name"):
            value = creator.get(key)
            if isinstance(value, str) and value.strip():
                selected[key] = value.strip()
        if selected:
            result.append(selected)
    return result


def metadata(item: dict[str, Any]) -> dict[str, Any]:
    data = _item_data(item)
    result: dict[str, Any] = {}
    for key in METADATA_KEYS:
        value = data.get(key, item.get(key))
        if key == "creators":
            value = _creator_metadata(value)
        if value not in (None, "", []):
            result[key] = value
    if "key" not in result and isinstance(item.get("key"), str):
        result["key"] = item["key"]
    return result


def _search_text(item: dict[str, Any]) -> str:
    data = _item_data(item)
    creators = data.get("creators", [])
    names = []
    if isinstance(creators, list):
        for creator in creators:
            if isinstance(creator, dict):
                names.extend(str(creator.get(key, "")) for key in ("firstName", "lastName", "name"))
    values = [data.get(key, "") for key in ("key", "title", "DOI", "publicationTitle", "itemType", "date")]
    return " ".join(str(value) for value in values + names if value).casefold()


def find_items(items: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
    needle = query.strip().casefold()
    if not needle:
        raise AdapterError("find_item query must not be empty")
    return [metadata(item) for item in items if needle in _search_text(item)]


def _find_one(items: list[dict[str, Any]], selector: str) -> dict[str, Any] | None:
    selected = selector.strip().casefold()
    for item in items:
        data = _item_data(item)
        key = str(data.get("key", item.get("key", ""))).casefold()
        if key == selected:
            return item
    matches = find_items(items, selector)
    return matches[0] if matches else None


def _bibtex_value(value: Any) -> str:
    if isinstance(value, list):
        parts = []
        for creator in value:
            if not isinstance(creator, dict):
                continue
            name = creator.get("name") or " ".join(filter(None, (creator.get("firstName"), creator.get("lastName"))))
            if name:
                parts.append(str(name))
        return " and ".join(parts)
    return str(value).replace("{", "\\{").replace("}", "\\}").replace("\n", " ").strip()


def to_bibtex(record: dict[str, Any]) -> str:
    key = re.sub(r"[^A-Za-z0-9._:-]+", "-", str(record.get("key", "item"))) or "item"
    item_type = "article" if record.get("publicationTitle") else "misc"
    mapping = {
        "title": "title",
        "creators": "author",
        "date": "year",
        "DOI": "doi",
        "publicationTitle": "journal",
        "journalAbbreviation": "journalabbr",
        "volume": "volume",
        "issue": "number",
        "pages": "pages",
        "publisher": "publisher",
        "url": "url",
    }
    fields = [f"  {target} = {{{_bibtex_value(record[source])}}}" for source, target in mapping.items() if record.get(source)]
    return "@{0}{{{1},\n{2}\n}}".format(item_type, key, ",\n".join(fields))


def _scrub(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): ("[REDACTED]" if SECRET_KEY.search(str(key)) else _scrub(item)) for key, item in value.items()}
    if isinstance(value, list):
        return [_scrub(item) for item in value]
    if isinstance(value, str) and SECRET_VALUE.search(value):
        return "[REDACTED]"
    return value


def execute(args: argparse.Namespace) -> dict[str, Any]:
    path = library_path(args.library_json)
    if args.command == "health":
        configured = path.is_file()
        return {"ok": True, "command": "health", "status": "configured" if configured else "not_configured", "configured": configured, "path": str(path)}
    if not path.is_file():
        return {"ok": True, "command": args.command, "status": "not_configured", "configured": False, "path": str(path)}
    items = _load_items(path)
    if args.command == "find_item":
        return {"ok": True, "command": "find_item", "status": "ok", "path": str(path), "items": find_items(items, args.query)}
    if args.command == "get_metadata":
        item = _find_one(items, args.selector)
        if item is None:
            return {"ok": False, "command": "get_metadata", "status": "not_found", "path": str(path), "error": "item not found"}
        return {"ok": True, "command": "get_metadata", "status": "ok", "path": str(path), "metadata": metadata(item)}
    if args.command == "export_bib":
        item = _find_one(items, args.selector)
        if item is None:
            return {"ok": False, "command": "export_bib", "status": "not_found", "path": str(path), "error": "item not found"}
        record = metadata(item)
        bibtex = to_bibtex(record)
        result: dict[str, Any] = {"ok": True, "command": "export_bib", "status": "ok", "path": str(path), "metadata": record, "bibtex": bibtex, "written": False}
        if args.output:
            output = _safe_path(args.output)
            if output.exists() and output.is_dir():
                raise AdapterError("export output must be a file")
            if not output.parent.is_dir():
                raise AdapterError("export output parent must already exist")
            output.write_text(bibtex + "\n", encoding="utf-8", newline="")
            result.update({"output_path": str(output), "written": True})
        return result
    raise AdapterError("unsupported command")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only Zotero metadata adapter")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("health",):
        child = sub.add_parser(command)
        child.add_argument("--library-json")
    for command in ("find_item", "get_metadata", "export_bib"):
        child = sub.add_parser(command)
        child.add_argument("selector" if command != "find_item" else "query")
        child.add_argument("--library-json")
        if command == "export_bib":
            child.add_argument("--output")
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
        print(f"{result.get('command', 'zotero')}: {result.get('status', 'ok')}")
    else:
        print(f"ERROR: {result.get('error', 'failed')}", file=sys.stderr)
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
