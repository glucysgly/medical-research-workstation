#!/usr/bin/env python3
"""Natural-language routing acceptance for the v5.1 control plane."""

from __future__ import annotations

import json
from pathlib import Path

from researchctl import ResearchCtl


ROOT = Path(__file__).resolve().parents[1]
PROMPTS = [
    ("新建一个临床研究项目", "clinical-observational"),
    ("继续这个课题", "project-resume-status"),
    ("检查这份数据", "structured"),
    ("分析这批 qPCR", "qpcr"),
    ("做系统综述", "systematic"),
    ("做 MR", "mr-gwas"),
    ("分析这个 GEO", "public-omics"),
    ("做单细胞分析", "scrna"),
    ("检查论文", "manuscript"),
    ("准备投稿", "manuscript"),
    ("复现上次分析", "reproduc"),
    ("看看所有项目现在卡在哪里", "project-resume-status"),
]


def main() -> int:
    ctl = ResearchCtl(ROOT)
    rows = []
    for prompt, expected in PROMPTS:
        result = ctl.command_route(prompt)
        actual = result.get("workflow_key")
        rows.append({"prompt": prompt, "expected": expected, "actual": actual, "primary_skill": result.get("primary_skill"), "task_code": result.get("task_code"), "status": "PASS" if actual == expected else "FAIL"})
    report = {"schema_version": "v5.1", "tests": rows, "summary": {"PASS": sum(row["status"] == "PASS" for row in rows), "FAIL": sum(row["status"] == "FAIL" for row in rows)}}
    (ROOT / "NATURAL_LANGUAGE_UX_REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Natural-language UX acceptance", "", "| Prompt | Expected workflow | Actual workflow | Primary skill | Status |", "|---|---|---|---|---|"]
    lines.extend(f"| {row['prompt']} | {row['expected']} | {row['actual']} | {row['primary_skill']} | {row['status']} |" for row in rows)
    lines.extend(["", f"Summary: `{report['summary']}`", "", "Routing only selects the workflow and gate; it does not claim that a scientific analysis ran."])
    (ROOT / "NATURAL_LANGUAGE_UX_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, sort_keys=True))
    return 0 if report["summary"]["FAIL"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
