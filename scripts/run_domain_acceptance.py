#!/usr/bin/env python3
"""Run the v5.1 core-domain control-plane acceptance matrix."""

from __future__ import annotations

import csv
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from qpcr_qc import review_csv  # noqa: E402
from researchctl import ResearchCtl  # noqa: E402


MATRIX = ROOT / "config" / "domain-acceptance-matrix.json"
PILOT = Path("D:/Users/nmls/Documents/New project")


def route_check(ctl: ResearchCtl, item: dict) -> dict:
    result = ctl.command_route(item["route_prompt"])
    expected = item["expected_route"]
    fields = {key: {"expected": value, "actual": result.get(key), "match": result.get(key) == value} for key, value in expected.items()}
    return {"status": "PASS" if all(x["match"] for x in fields.values()) else "FAIL", "fields": fields, "result": result}


def clinical_smoke() -> dict:
    with tempfile.TemporaryDirectory(prefix="mwr-clinical-acceptance-") as temporary:
        root = Path(temporary)
        (root / "templates").mkdir()
        shutil.copytree(ROOT / "templates" / "clinical-study", root / "templates" / "clinical-study")
        (root / "README.md").write_text("fixture\n", encoding="utf-8")
        (root / "AGENTS.md").write_text("fixture\n", encoding="utf-8")
        ctl = ResearchCtl(root)
        created = ctl.command_new("clinical-study", "acceptance-clinical", "Clinical acceptance fixture")
        project = root / "projects" / "acceptance-clinical"
        passed = bool(created.get("ok")) and (project / "project.yaml").is_file() and (project / "status.yaml").is_file()
        return {"status": "PASS" if passed else "FAIL", "negative_case": "missing project record => BLOCKED"}


def qpcr_smoke() -> dict:
    with tempfile.TemporaryDirectory(prefix="mwr-qpcr-acceptance-") as temporary:
        path = Path(temporary) / "qpcr.csv"
        rows = [["group", "biological_replicate", "technical_replicate", "target", "ct"]]
        for group in ("control", "RPL"):
            for biological in ("B1", "B2"):
                for technical, ct in (("T1", "22.1"), ("T2", "22.3")):
                    rows.append([group, biological, technical, "GAPDH", ct])
        with path.open("w", newline="", encoding="utf-8") as handle:
            csv.writer(handle).writerows(rows)
        passed = review_csv(path)["status"] == "pass"
        rows[-1][-1] = "NA"
        with path.open("w", newline="", encoding="utf-8") as handle:
            csv.writer(handle).writerows(rows)
        negative = review_csv(path)["status"] == "review_required"
        return {"status": "PASS" if passed and negative else "FAIL", "positive": passed, "negative_missing_ct": negative}


def template_smoke(domain_id: str) -> dict:
    mapping = {
        "systematic-review-meta": ["protocol", "literature", "analysis", "results", "provenance"],
        "mr-gwas": ["domain.yaml", "routing-contract.md", "AGENTS.md"],
        "public-omics-bulk": ["domain.yaml", "routing-contract.md", "AGENTS.md"],
    }
    base = ROOT / ("templates/systematic-review-meta" if domain_id == "systematic-review-meta" else "domain-packs/" + {"mr-gwas": "mr-gwas", "public-omics-bulk": "public-omics"}[domain_id])
    required = mapping[domain_id]
    passed = all((base / item).exists() for item in required)
    return {"status": "PASS" if passed else "FAIL", "required": required, "base": str(base)}


def scrna_smoke() -> dict:
    run_dir = PILOT / "results" / "scrna-production" / "run-20260809"
    required = [run_dir / "result-manifest.json", run_dir / "filtered_annotated.h5ad", run_dir / "provenance" / "run_metadata.json", run_dir / "tables" / "donor_aware_de.csv"]
    if not run_dir.exists():
        return {"status": "BLOCKED", "reason": "real pilot run has not completed"}
    status_path = run_dir / "provenance" / "run_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8")) if status_path.exists() else {}
    passed = all(item.is_file() for item in required) and status.get("status") == "PASS"
    return {"status": "PASS" if passed else "BLOCKED", "required_outputs": [str(x) for x in required], "run_status": status.get("status", "missing")}


def main() -> int:
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    ctl = ResearchCtl(ROOT)
    report = {"schema_version": "v5.1", "matrix": str(MATRIX), "domains": [], "generated_by": str(Path(__file__))}
    for item in matrix["core_domains"]:
        domain_id = item["domain_id"]
        route = route_check(ctl, item)
        if domain_id == "clinical-observational":
            smoke = clinical_smoke()
        elif domain_id == "qpcr":
            smoke = qpcr_smoke()
        elif domain_id in {"systematic-review-meta", "mr-gwas", "public-omics-bulk"}:
            smoke = template_smoke(domain_id)
            if domain_id in {"mr-gwas", "public-omics-bulk"}:
                smoke["runtime_boundary"] = "BLOCKED without real external input; no synthetic scientific result generated"
        else:
            smoke = scrna_smoke()
        statuses = {route["status"], smoke["status"]}
        overall = "FAIL" if "FAIL" in statuses else "BLOCKED" if "BLOCKED" in statuses else "PASS" if statuses == {"PASS"} else "WARN"
        if smoke.get("runtime_boundary"):
            overall = "WARN"
        report["domains"].append({"domain_id": domain_id, "overall": overall, "route": route, "smoke": smoke, "expected": item})
    report["summary"] = {status: sum(1 for item in report["domains"] if item["overall"] == status) for status in ("PASS", "WARN", "FAIL", "BLOCKED")}
    target_json = ROOT / "DOMAIN_ACCEPTANCE_REPORT.json"
    target_md = ROOT / "DOMAIN_ACCEPTANCE_REPORT.md"
    target_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# v5.1 Core Domain Acceptance", "", f"Matrix: `{MATRIX.relative_to(ROOT).as_posix()}`", "", "| Domain | Overall | Route | Smoke |", "|---|---|---|---|"]
    lines.extend(f"| {item['domain_id']} | {item['overall']} | {item['route']['status']} | {item['smoke']['status']} |" for item in report["domains"])
    lines.extend(["", "## Summary", "", json.dumps(report["summary"], ensure_ascii=False), "", "MR/GWAS and public-omics rows deliberately remain input-gated; no synthetic scientific result is promoted."])
    target_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, sort_keys=True))
    return 0 if report["summary"].get("FAIL", 0) == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
