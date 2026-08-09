#!/usr/bin/env python3
"""Read-only qPCR CSV quality review with biological-replicate statistics."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


class QpcrQcError(Exception):
    """Expected, user-facing qPCR QC error."""


ALIASES = {
    "group": {"group", "condition", "treatment", "samplegroup", "experimentalgroup"},
    "biological_replicate": {"biologicalreplicate", "bioreplicate", "biorep", "sample", "sampleid"},
    "technical_replicate": {"technicalreplicate", "techreplicate", "techrep", "well", "wellid"},
    "target": {"target", "gene", "assay", "targetgene"},
    "ct": {"ct", "cq", "cyclethreshold"},
}
REQUIRED = tuple(ALIASES)


def _header_key(value: str) -> str:
    return "".join(character for character in value.casefold() if character.isalnum())


def _column_map(fieldnames: list[str] | None) -> tuple[dict[str, str], list[str]]:
    fields = fieldnames or []
    normalized = {_header_key(field): field for field in fields if field}
    mapping = {}
    missing = []
    for canonical, aliases in ALIASES.items():
        source = next((normalized[alias] for alias in aliases if alias in normalized), None)
        if source is None:
            missing.append(canonical)
        else:
            mapping[canonical] = source
    return mapping, missing


def _issue(kind: str, **details: Any) -> dict[str, Any]:
    return {"type": kind, **details}


def review_csv(path: str | Path, *, min_ct: float = 0.0, max_ct: float = 45.0) -> dict[str, Any]:
    input_path = Path(path).expanduser().resolve(strict=False)
    if not input_path.is_file():
        raise QpcrQcError("input CSV is not a readable file")
    try:
        with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            mapping, missing = _column_map(reader.fieldnames)
            rows = list(reader)
    except (OSError, UnicodeError, csv.Error) as exc:
        raise QpcrQcError(f"unable to read CSV: {type(exc).__name__}") from exc

    issues: list[dict[str, Any]] = [_issue("missing_required_column", column=column) for column in missing]
    counts: dict[str, set[str]] = defaultdict(set)
    technical_keys: Counter[tuple[str, str, str, str]] = Counter()
    if not missing:
        for line_number, row in enumerate(rows, 2):
            values = {key: str(row.get(source, "") or "").strip() for key, source in mapping.items()}
            for field in ("group", "biological_replicate", "technical_replicate", "target"):
                if not values[field]:
                    issues.append(_issue("missing_value", field=field, row=line_number))
            if values["group"] and values["biological_replicate"]:
                counts[values["group"]].add(values["biological_replicate"])
            technical_key = (values["group"], values["biological_replicate"], values["technical_replicate"], values["target"])
            if all(technical_key):
                technical_keys[technical_key] += 1
            raw_ct = values["ct"]
            if not raw_ct or raw_ct.casefold() in {"na", "n/a", "nan", "nd", "undetermined", "missing"}:
                issues.append(_issue("missing_ct", row=line_number))
                continue
            try:
                ct = float(raw_ct)
            except ValueError:
                issues.append(_issue("invalid_ct", row=line_number))
                continue
            if not math.isfinite(ct) or ct < min_ct or ct > max_ct:
                issues.append(_issue("ct_out_of_range", row=line_number, value=raw_ct, minimum=min_ct, maximum=max_ct))
        for key, repetitions in sorted(technical_keys.items()):
            if repetitions > 1:
                group, biological, technical, target = key
                issues.append(
                    _issue(
                        "duplicate_technical_replicate",
                        group=group,
                        biological_replicate=biological,
                        technical_replicate=technical,
                        target=target,
                        rows=repetitions,
                    )
                )

    biological_counts = {group: len(replicates) for group, replicates in sorted(counts.items())}
    checklist = {
        "required_columns_present": not missing,
        "biological_replicates_identifiable": not missing and not any(issue["type"] == "missing_value" and issue["field"] == "biological_replicate" for issue in issues),
        "technical_replicates_not_statistical_n": True,
        "technical_replicate_ids_unique_within_biological_target": not any(issue["type"] == "duplicate_technical_replicate" for issue in issues),
        "ct_values_complete": not any(issue["type"] == "missing_ct" for issue in issues),
        "ct_values_within_configured_range": not any(issue["type"] in {"invalid_ct", "ct_out_of_range"} for issue in issues),
        "per_group_biological_n_reported": not missing,
        "raw_input_unchanged_by_this_review": True,
        "reference_gene_and_assay_efficiency_review_required": True,
    }
    return {
        "ok": not issues,
        "status": "pass" if not issues else "review_required",
        "input_path": str(input_path),
        "statistical_unit": "biological_replicate",
        "technical_replicate_role": "within-biological-replicate QC only",
        "rows": len(rows),
        "required_columns": list(REQUIRED),
        "missing_required_columns": missing,
        "biological_replicate_counts": biological_counts,
        "issues": issues,
        "miqe_review_checklist": checklist,
    }


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only qPCR QC review")
    parser.add_argument("input_path", nargs="?")
    parser.add_argument("--input", dest="input_option")
    parser.add_argument("--min-ct", type=float, default=0.0)
    parser.add_argument("--max-ct", type=float, default=45.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in raw or "-j" in raw
    raw = [item for item in raw if item not in {"--json", "-j"}]
    try:
        args = make_parser().parse_args(raw)
        input_path = args.input_option or args.input_path
        if not input_path:
            raise QpcrQcError("an input CSV is required")
        result = review_csv(input_path, min_ct=args.min_ct, max_ct=args.max_ct)
    except (QpcrQcError, OSError, ValueError) as exc:
        result = {"ok": False, "status": "error", "error": str(exc)}
    if as_json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    elif result.get("ok"):
        print("qpcr_qc: PASS")
    else:
        print(f"qpcr_qc: {result.get('status', 'error')}")
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
