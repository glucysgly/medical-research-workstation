#!/usr/bin/env python3
"""Small, deterministic, standard-library-only research workstation CLI.

The command intentionally keeps scientific decisions outside the tool.  It
creates and checks portable text records, never edits data/raw, and avoids
printing file contents (especially values that may be private or secret).
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import os
import platform
import re
import shutil
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = 1
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
SECRET_KEY = re.compile(r"(?i)(api[_-]?key|access[_-]?token|password|passwd|secret|cookie|authorization|^token$)")
SECRET_VALUE = re.compile(
    r"(?is)(?:api[_-]?key|access[_-]?token|password|passwd|secret|cookie|authorization)\s*[:=]\s*[^\s,;]+"
    r"|AKIA[0-9A-Z]{16}|-----BEGIN [^-]+-----|eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+"
)
PHI_HEADER = re.compile(r"(?i)^(patient|subject|participant|病例|患者|身份证|姓名|phone|email|address|mrn)")
V5_STATUS_STAGES = {
    "IDEA",
    "QUESTION",
    "LITERATURE",
    "PROTOCOL",
    "DATA_INTAKE",
    "DATA_QC",
    "ANALYSIS_PLAN",
    "ANALYSIS",
    "RESULTS_QC",
    "INTERPRETATION",
    "MANUSCRIPT",
    "MANUSCRIPT_QC",
    "SUBMISSION",
    "REVISION",
    "ARCHIVE",
}
STATUS_VALUES = V5_STATUS_STAGES | {"planned", "active", "paused", "completed", "archived"}
STATUS_ALIASES = {"in-progress": "active", "in_progress": "active", "done": "completed"}
SAFE_POLICY_FIELDS = {
    "secret_output",
    "secret_output_allowed",
    "no_secret_output",
    "secret_file_count",
    "potential_phi_header_count",
    "unreadable_file_count",
}
PLACEHOLDER_NAMES = {"README.md", ".gitkeep"}


class ResearchCtlError(Exception):
    """Expected user-facing failure without a traceback."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_id(value: str) -> str:
    if not SAFE_ID.fullmatch(value):
        raise ResearchCtlError("project id must use 1-64 ASCII letters, digits, '.', '_' or '-'")
    return value


def split_inline(value: str) -> list[str]:
    result: list[str] = []
    current: list[str] = []
    quote = ""
    depth = 0
    for char in value:
        if quote:
            current.append(char)
            if char == quote:
                quote = ""
        elif char in "'\"":
            quote = char
            current.append(char)
        elif char in "[{(":
            depth += 1
            current.append(char)
        elif char in "]})":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            result.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if current or value.strip():
        result.append("".join(current).strip())
    return result


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return None
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if (value.startswith("\"") and value.endswith("\"")) or (value.startswith("'") and value.endswith("'")):
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        return [parse_scalar(item) for item in split_inline(value[1:-1])]
    if value.startswith("{") and value.endswith("}"):
        parsed: dict[str, Any] = {}
        for item in split_inline(value[1:-1]):
            if ":" in item:
                key, item_value = item.split(":", 1)
                parsed[str(parse_scalar(key.strip()))] = parse_scalar(item_value)
        return parsed
    try:
        if re.fullmatch(r"[-+]?\d+", value):
            return int(value)
        if re.fullmatch(r"[-+]?(?:\d+\.\d*|\d*\.\d+)", value):
            return float(value)
    except ValueError:
        pass
    return value


def _yaml_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        content = raw.strip()
        if " #" in content:
            content = content.split(" #", 1)[0].rstrip()
        lines.append((indent, content))
    return lines


def parse_yaml(text: str) -> Any:
    """Parse the small YAML subset used by workstation metadata/config files."""
    lines = _yaml_lines(text)
    if not lines:
        return {}

    def block(index: int, indent: int) -> tuple[Any, int]:
        if index >= len(lines):
            return {}, index
        is_list = lines[index][0] == indent and lines[index][1].startswith("-")
        output: Any = [] if is_list else {}
        while index < len(lines) and lines[index][0] == indent:
            content = lines[index][1]
            if is_list:
                if not content.startswith("-"):
                    break
                item = content[1:].strip()
                index += 1
                if not item:
                    if index < len(lines) and lines[index][0] > indent:
                        value, index = block(index, lines[index][0])
                    else:
                        value = None
                elif ":" in item and not item.startswith(("http://", "https://")):
                    key, raw_value = item.split(":", 1)
                    value = {key.strip(): parse_scalar(raw_value)}
                    if index < len(lines) and lines[index][0] > indent:
                        extra, index = block(index, lines[index][0])
                        if isinstance(extra, dict):
                            value.update(extra)
                else:
                    value = parse_scalar(item)
                output.append(value)
            else:
                if content.startswith("-") or ":" not in content:
                    break
                key, raw_value = content.split(":", 1)
                key = key.strip().strip("'\"")
                index += 1
                if raw_value.strip():
                    value = parse_scalar(raw_value)
                elif index < len(lines) and lines[index][0] > indent:
                    value, index = block(index, lines[index][0])
                else:
                    value = None
                output[key] = value
        return output, index

    value, _ = block(0, lines[0][0])
    return value


def load_text_record(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return parse_yaml(text)


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if not text or re.search(r"[:#\[\]{},]|^[-?]$|\s$", text) or text.lower() in {"true", "false", "null"}:
        return json.dumps(text, ensure_ascii=False)
    return text


def dump_yaml(value: Any, indent: int = 0) -> str:
    spaces = " " * indent
    lines: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{spaces}{key}:")
                lines.append(dump_yaml(item, indent + 2).rstrip("\n"))
            else:
                lines.append(f"{spaces}{key}: {yaml_scalar(item)}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                first = True
                for key, child in item.items():
                    if isinstance(child, (dict, list)):
                        lines.append(f"{spaces}- {key}:")
                        lines.append(dump_yaml(child, indent + 4).rstrip("\n"))
                    else:
                        prefix = f"{spaces}- " if first else " " * (indent + 2)
                        lines.append(f"{prefix}{key}: {yaml_scalar(child)}")
                    first = False
            else:
                lines.append(f"{spaces}- {yaml_scalar(item)}")
    else:
        lines.append(f"{spaces}{yaml_scalar(value)}")
    return "\n".join(lines) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def write_yaml(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(dump_yaml(value), encoding="utf-8")
    os.replace(temporary, path)


def scrub(value: Any) -> Any:
    """Remove secret-like fields and redact secret-like text without echoing it."""
    if isinstance(value, dict):
        output: dict[str, Any] = {}
        for key, item in value.items():
            if str(key) not in SAFE_POLICY_FIELDS and SECRET_KEY.search(str(key)):
                output[str(key)] = "[REDACTED]"
            else:
                output[str(key)] = scrub(item)
        return output
    if isinstance(value, list):
        return [scrub(item) for item in value]
    if isinstance(value, str) and SECRET_VALUE.search(value):
        return "[REDACTED]"
    return value


class ResearchCtl:
    def __init__(self, root: Path | None = None):
        configured = root or os.environ.get("RESEARCHCTL_ROOT")
        self.root = Path(configured).resolve() if configured else Path(__file__).resolve().parents[1]
        self.projects_root = self.root / "projects"

    def project_path(self, project_id: str) -> Path:
        project_id = safe_id(project_id)
        candidates = [self.projects_root / project_id, self.root / project_id]
        for candidate in candidates:
            if (candidate / "project.yaml").is_file():
                return candidate.resolve()
        raise ResearchCtlError(f"project not found: {project_id}")

    def project_records(self) -> list[dict[str, Any]]:
        candidates: list[Path] = []
        for base in (self.projects_root, self.root):
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir(), key=lambda path: path.name.lower()):
                if child.is_dir() and (child / "project.yaml").is_file() and child not in candidates:
                    candidates.append(child)
        records = []
        for path in candidates:
            metadata = load_text_record(path / "project.yaml", {}) or {}
            status = load_text_record(path / "status.yaml", {}) or {}
            records.append(
                {
                    "id": metadata.get("project_id", path.name),
                    "title": metadata.get("title", path.name),
                    "template": metadata.get("template", "unknown"),
                    "privacy_level": metadata.get("privacy_level", "restricted"),
                    "status": status.get("status", "unknown"),
                    "path": str(path),
                }
            )
        return records

    def command_doctor(self) -> dict[str, Any]:
        required = ["README.md", "AGENTS.md", "config/workstation.yaml", "config/skill-index.yaml"]
        checks = {path: (self.root / path).is_file() for path in required}
        checks["projects_directory"] = self.projects_root.is_dir()
        global_index = load_text_record(self.root / "config/workstation.yaml", {}) or {}
        integration_path = ((global_index.get("integrations") or {}).get("global_capability_index"))
        if integration_path:
            checks["global_capability_index"] = Path(integration_path).expanduser().is_file()
        tools = {name: bool(shutil.which(name)) for name in ("python", "git", "quarto", "pandoc")}
        # The projects directory is created lazily by ``new``; a clean
        # workstation is healthy before its first project exists.
        failures = [name for name, passed in checks.items() if not passed and name != "projects_directory"]
        return {
            "ok": not failures,
            "command": "doctor",
            "schema_version": SCHEMA_VERSION,
            "root": str(self.root),
            "checks": checks,
            "tools": tools,
            "python": platform.python_version(),
            "failures": failures,
            "privacy": {"raw_data_immutable": True, "secret_output": False, "external_upload": "blocked"},
        }

    def command_skills_audit(self) -> dict[str, Any]:
        path = self.root / "config" / "skill-index.yaml"
        data = load_text_record(path, {}) or {}
        skills = data.get("skills") if isinstance(data, dict) else None
        failures: list[str] = []
        names: list[str] = []
        if not isinstance(skills, list):
            failures.append("skills list missing")
            skills = []
        for index, skill in enumerate(skills):
            if not isinstance(skill, dict):
                failures.append(f"skill[{index}] is not a mapping")
                continue
            name = skill.get("name")
            if not name or name in names:
                failures.append(f"skill[{index}] has missing or duplicate name")
            else:
                names.append(str(name))
            if not skill.get("category"):
                failures.append(f"skill[{index}] category missing")
            if not isinstance(skill.get("triggers"), list) or not skill.get("triggers"):
                failures.append(f"skill[{index}] triggers missing")
        return {
            "ok": not failures,
            "command": "skills audit",
            "schema_version": SCHEMA_VERSION,
            "path": str(path),
            "skill_count": len(skills),
            "skills": names,
            "failures": failures,
        }

    def command_projects(self) -> dict[str, Any]:
        records = self.project_records()
        return {"ok": True, "command": "projects", "count": len(records), "projects": records}

    def command_new(self, template: str, project_id: str, title: str) -> dict[str, Any]:
        project_id = safe_id(project_id)
        if not template or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", template):
            raise ResearchCtlError("template must use ASCII letters, digits, '.', '_' or '-'")
        destination = self.projects_root / project_id
        if destination.exists() and any(destination.iterdir()):
            raise ResearchCtlError(f"project already exists: {project_id}")
        destination.mkdir(parents=True, exist_ok=True)
        source = self.root / "templates" / template
        if source.is_dir():
            for item in source.rglob("*"):
                relative = item.relative_to(source)
                target = destination / relative
                if item.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, target)
        for relative in (
            "data/raw",
            "data/manifests",
            "analysis",
            "results",
            "literature",
            "provenance/runs",
            "reports",
            "logs",
            "scripts",
        ):
            (destination / relative).mkdir(parents=True, exist_ok=True)
        template_metadata = load_text_record(source / "project.yaml", {}) if source.is_dir() else {}
        if not isinstance(template_metadata, dict):
            template_metadata = {}
        now = utc_now()
        metadata = dict(template_metadata)
        metadata.update(
            {
                "schema_version": "v5",
                "project_id": project_id,
                "title": title,
                "short_name": project_id,
                "type": template,
                "template": template,
                "status": "IDEA",
                "privacy_level": "restricted",
                "raw_data_immutable": True,
                "created_at": now,
                "updated_at": now,
                "source_of_truth": ["project.yaml", "status.yaml", "data/manifests", "provenance"],
            }
        )
        template_status = load_text_record(source / "status.yaml", {}) if source.is_dir() else {}
        if not isinstance(template_status, dict):
            template_status = {}
        status = dict(template_status)
        status.update(
            {
                "schema_version": "v5",
                "project_id": project_id,
                "status": "IDEA",
                "stage": "IDEA",
                "state": "idea",
                "updated_at": now,
                "status_history": [{"status": "IDEA", "reason": "project created", "at": now}],
            }
        )
        write_yaml(destination / "project.yaml", metadata)
        write_yaml(destination / "status.yaml", status)
        readme = f"# {title}\n\nTemplate: `{template}`\n\nRaw data is immutable and remains under `data/raw/`.\n"
        (destination / "README.md").write_text(readme, encoding="utf-8")
        return {"ok": True, "command": "new", "project": {"id": project_id, "title": title, "template": template, "path": str(destination)}}

    def command_status(self, project_id: str, new_status: str | None = None, reason: str | None = None) -> dict[str, Any]:
        path = self.project_path(project_id)
        record_path = path / "status.yaml"
        record = load_text_record(record_path, {}) or {}
        current = str(record.get("status", "IDEA"))
        if new_status is not None:
            new_status = STATUS_ALIASES.get(new_status, new_status)
            if new_status.upper() in V5_STATUS_STAGES:
                new_status = new_status.upper()
            if new_status not in STATUS_VALUES:
                raise ResearchCtlError(f"unsupported status: {new_status}")
            if not reason or not reason.strip():
                raise ResearchCtlError("status changes require --reason")
            history = record.get("status_history") if isinstance(record.get("status_history"), list) else []
            history.append({"status": new_status, "from": current, "reason": reason.strip(), "at": utc_now()})
            record.update(
                {
                    "schema_version": "v5",
                    "project_id": project_id,
                    "status": new_status,
                    "stage": new_status if new_status in V5_STATUS_STAGES else record.get("stage"),
                    "state": new_status.lower(),
                    "updated_at": utc_now(),
                    "status_history": history,
                }
            )
            write_yaml(record_path, record)
            current = new_status
        return {"ok": True, "command": "status", "project_id": project_id, "status": current, "status_history": record.get("status_history", [])}

    def command_route(self, query: str) -> dict[str, Any]:
        lowered = query.lower()
        routes = [
            ("remove-ai-marks", "DOC", ("水印", "去除水印", "清理水印", "c2pa", "content credentials", "exif", "xmp", "ai metadata", "不可见字符", "remove ai marks", "remove watermark"), ["security-and-hardening"], "artifact-mark-cleaning"),
            ("humanizer-zh", "RESEARCH", ("中文去ai味", "去 ai 味", "去ai味", "去掉 ai 味", "去掉ai味", "中文去痕", "中文人性化", "中文自然改写", "humanizer-zh"), ["nature-reviewer"], "manuscript-humanization-zh"),
            ("humanizer", "RESEARCH", ("english humanize", "humanize english", "humanize this", "remove ai writing", "de-ai prose", "english 去ai味", "english 去痕", "humanizer"), ["nature-reviewer"], "manuscript-humanization-en"),
            ("recreate-scientific-figure-in-drawio", "DESIGN", ("科研图重绘", "重绘科研图", "科研插图", "科学插图", "可编辑底稿", "可编辑科研图", "ai生成的科研图", "drawio", "draw.io", "scientific illustrator", "scientific figure redraw", "recreate scientific figure", "editable drawio", "editable scientific figure"), ["nature-figure"], "scientific-figure-drawio-redraw"),
            ("design-taste-frontend", "DESIGN", ("科研网站", "研究门户", "landing page", "research landing page", "research website redesign", "前端反模板", "视觉反套路", "design taste"), ["web-design-guidelines"], "research-web-design"),
            ("life-science-evidence-review", "RESEARCH", ("生命科学综述", "生命科学证据综述", "文献综述", "证据综述", "evidence synthesis", "research overview", "literature review", "gene review", "pathway review", "gene family review", "knowledge gap analysis", "research roadmap"), ["nature-academic-search", "nature-citation"], "life-science-evidence-review"),
            ("evidence-bound-natural-science-writing", "RESEARCH", ("evidence-bound writing", "evidence ceiling", "claim ceiling", "natural-science manuscript", "natural science paper", "scientific manuscript revision", "自然科学论文", "自然科学稿件", "论文证据边界", "证据约束型修订", "defensive scientific writing", "overclaiming", "association versus causation", "关联与因果", "机制已证实", "validated biomarker", "internal validation", "discordant datasets", "evidence contract", "claim evidence audit", "主张证据审计"), ["avoid-overkill", "nature-citation"], "evidence-bound-natural-science-writing"),
            ("avoid-overkill", "RESEARCH", ("论文不要自我削弱", "自我削弱式写作", "防御性写作", "不要替审稿人检讨", "预写审稿意见", "删除预写审稿意见", "删除自我削弱", "删除审稿人预设", "论文改得更主动", "论文主动", "去自我削弱", "claim-centered", "defensive writing", "self-weakening", "reviewer objections", "发布会原则"), ["nature-citation"], "proportional-academic-writing"),
            ("avoid-overkill", "DEV", ("代码过度封装", "避免过度工程", "不要过度封装", "不要加抽象", "不新增抽象", "不要加静默降级", "静默降级", "不要堆测试补丁", "测试补丁", "不要加无谓校验", "工程最小改动", "最小修复", "overengineering", "minimal coherent change", "test patching", "silent fallback", "unnecessary abstraction", "proportional coding"), ["diagnosing-bugs"], "proportional-engineering"),
            ("avoid-overkill", "DEV", ("不要过度设计", "别过度设计", "避免范围蔓延", "不要过度服务", "不要想太多", "keep it proportional", "keep it minimal", "stop overthinking", "avoid overkill"), ["diagnosing-bugs"], "proportionality-control"),
            ("nature-academic-search", "RESEARCH", ("临床研究", "临床试验", "队列", "病例对照", "observational", "cohort"), ["data-analytics:validate-data"], "clinical-observational"),
            ("research", "RESEARCH", ("继续这个课题", "继续课题", "resume", "continue", "项目状态", "所有项目", "卡在哪里"), ["superpowers:verification-before-completion"], "project-resume-status"),
            ("data-analytics:validate-data", "DATA", ("检查这份数据", "检查数据", "数据质控"), ["data-analytics:analyze-data-quality"], "structured"),
            ("data-analytics:validate-data", "BIO", ("qpcr", "ct", "ddct", "delta ct", "定量pcr", "荧光定量"), ["nature-data"], "qpcr"),
            ("nature-academic-search", "RESEARCH", ("systematic review", "系统综述", "meta-analysis", "meta分析", "荟萃", "prisma", "screening", "筛选"), ["literature-downloader"], "systematic"),
            ("research", "BIO", ("mendelian", "孟德尔随机化", "mr", "gwas", "工具变量", "harmoniz"), ["life-science-research:gwas-catalog-skill"], "mr-gwas"),
            ("ngs-analysis:scrna-seq-qc", "BIO", ("单细胞", "single-cell", "scrna"), ["ngs-analysis:ngs-runtime-env"], "scrna"),
            ("ngs-analysis:ngs-analysis-router", "BIO", ("geo", "rna-seq", "转录组", "transcriptome", "omics", "组学"), ["ngs-analysis:ngs-runtime-env", "data-analytics:validate-data"], "public-omics"),
            ("nature-reviewer", "RESEARCH", ("检查论文", "论文质控", "manuscript qc", "结果数字", "前后矛盾", "inconsistency", "table", "figure", "投稿", "返修", "submission"), ["nature-citation"], "manuscript"),
            ("nature-academic-search", "RESEARCH", ("literature", "文献", "evidence", "证据", "guideline", "指南", "paper", "论文", "doi", "pmid"), ["literature-downloader", "zotero-deduplicated-import"], "literature"),
            ("superpowers:verification-before-completion", "RESEARCH", ("reproduce", "复现", "provenance", "溯源", "lockfile", "environment", "环境", "render", "渲染", "可重复"), ["context-mode:ctx-doctor"], "reproduc"),
            ("security-and-hardening", "RESEARCH", ("phi", "pii", "secret", "privacy", "隐私", "患者", "个人信息", "upload", "上传"), [], "privacy"),
            ("data-analytics:validate-data", "DATA", ("qc", "质控", "missing", "缺失", "duplicate", "重复", "unit", "单位", "outlier", "异常值"), ["data-analytics:analyze-data-quality"], "structured"),
        ]
        selected = next((item for item in routes if any(token in lowered for token in item[2])), None)
        if selected is None:
            selected = ("nature-academic-search", "RESEARCH", (), [], "literature")
        primary, task_code, _, supporting, workflow_key = selected
        capability = None
        capability_path = self.root / "registry" / "RESEARCH_CAPABILITY_VIEW.csv"
        if capability_path.is_file():
            with capability_path.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            normalized_workflow = workflow_key.replace("-", " ").lower()
            capability = next(
                (row for row in rows if normalized_workflow in str(row.get("workflow", "")).lower()),
                None,
            )
            if capability is None:
                capability = next((row for row in rows if primary == row.get("primary_skill")), None)
        result = {
            "ok": True,
            "command": "route",
            "query": query,
            "task_code": task_code,
            "primary_skill": primary,
            "supporting_skills": supporting,
            "workflow_key": workflow_key,
            "risk_gate": "human-decision-gate" if primary in {"security-and-hardening", "remove-ai-marks"} else "research-integrity",
            "capability_view": "registry/RESEARCH_CAPABILITY_VIEW.csv",
        }
        if capability:
            result["workflow"] = workflow_key
            result["capability_workflow"] = capability.get("workflow")
            result["execution_layer"] = capability.get("execution_layer")
            result["preconditions"] = capability.get("preconditions")
            result["minimum_validation"] = capability.get("verification")
        else:
            result["workflow"] = workflow_key
        return result

    def _raw_files(self, path: Path) -> Iterable[Path]:
        raw = path / "data" / "raw"
        if not raw.is_dir():
            return []
        return (
            item
            for item in sorted(raw.rglob("*"))
            if item.is_file() and not item.is_symlink() and item.name not in PLACEHOLDER_NAMES
        )

    def _privacy_scan(self, path: Path) -> dict[str, Any]:
        secret_files = 0
        phi_headers = 0
        unreadable = 0
        for item in self._raw_files(path):
            try:
                sample = item.read_bytes()[:2 * 1024 * 1024]
            except OSError:
                unreadable += 1
                continue
            text = sample.decode("utf-8", errors="ignore")
            if SECRET_VALUE.search(text):
                secret_files += 1
            if item.suffix.lower() in {".csv", ".tsv"}:
                first = text.splitlines()[0] if text.splitlines() else ""
                fields = re.split(r"[,\t]", first)
                phi_headers += sum(1 for field in fields if PHI_HEADER.search(field.strip()))
        return {"secret_file_count": secret_files, "potential_phi_header_count": phi_headers, "unreadable_file_count": unreadable, "status": "review_required" if secret_files or phi_headers else "pass"}

    def _manifest(self, path: Path, project_id: str) -> tuple[dict[str, Any], str]:
        files = []
        for item in self._raw_files(path):
            relative = item.relative_to(path).as_posix()
            files.append({"path": relative, "size": item.stat().st_size, "sha256": sha256_file(item)})
        body = {"schema_version": "v5", "project_id": project_id, "raw_data_policy": "immutable", "files": files}
        digest = sha256_bytes(canonical_json(body))
        manifest = dict(body)
        manifest["manifest_sha256"] = digest
        return manifest, digest

    def _verify_manifest(self, path: Path, manifest: dict[str, Any]) -> dict[str, Any]:
        expected = manifest.get("manifest_sha256")
        body = {key: manifest.get(key) for key in ("schema_version", "project_id", "raw_data_policy", "files")}
        checks: list[dict[str, Any]] = []
        for entry in manifest.get("files", []):
            relative = str(entry.get("path", ""))
            file_path = (path / relative).resolve()
            inside = path.resolve() in file_path.parents
            exists = inside and file_path.is_file() and not file_path.is_symlink()
            actual = sha256_file(file_path) if exists else None
            checks.append({"path": relative, "exists": exists, "unchanged": exists and actual == entry.get("sha256")})
        return {"manifest_hash_valid": expected == sha256_bytes(canonical_json(body)), "files": checks, "valid": expected == sha256_bytes(canonical_json(body)) and all(item["unchanged"] for item in checks)}

    def command_qc(self, project_id: str) -> dict[str, Any]:
        path = self.project_path(project_id)
        started = time.perf_counter()
        manifest, manifest_digest = self._manifest(path, project_id)
        privacy = self._privacy_scan(path)
        csv_checks = []
        for item in self._raw_files(path):
            if item.suffix.lower() not in {".csv", ".tsv"}:
                continue
            delimiter = "\t" if item.suffix.lower() == ".tsv" else ","
            try:
                with item.open("r", encoding="utf-8-sig", newline="") as handle:
                    rows = list(csv.reader(handle, delimiter=delimiter))
                header = rows[0] if rows else []
                duplicate_columns = sorted({field for field in header if field and header.count(field) > 1})
                missing_cells = sum(1 for row in rows[1:] for cell in row if not cell.strip())
                csv_checks.append({"path": item.relative_to(path).as_posix(), "rows": max(0, len(rows) - 1), "columns": len(header), "duplicate_columns": duplicate_columns, "missing_cells": missing_cells})
            except (OSError, UnicodeError, csv.Error):
                csv_checks.append({"path": item.relative_to(path).as_posix(), "readable": False})
        qc = {"schema_version": "v5", "project_id": project_id, "manifest_sha256": manifest_digest, "privacy": privacy, "csv": csv_checks, "raw_file_count": len(manifest["files"]), "status": "review_required" if privacy["status"] != "pass" else "pass", "generated_at": utc_now()}
        write_json(path / "data" / "manifests" / "raw-manifest.json", manifest)
        write_json(path / "data" / "manifests" / "qc-report.json", qc)
        run_id = utc_now().replace("-", "").replace(":", "").replace("T", "-").replace("Z", "") + "-" + manifest_digest[:12]
        output_rel = "data/manifests/qc-report.json"
        run = {
            "schema_version": "v5",
            "run_id": run_id,
            "project_id": project_id,
            "timestamp": utc_now(),
            "created_at": utc_now(),
            "git_commit": None,
            "working_tree_status": "not_git_repository",
            "input_hashes": {"data/manifests/raw-manifest.json": manifest_digest},
            "scripts": ["scripts/researchctl.py"],
            "command": "researchctl qc",
            "runtime_versions": {"python": platform.python_version()},
            "lock_hashes": {},
            "seed": None,
            "input_manifest": "data/manifests/raw-manifest.json",
            "input_manifest_sha256": manifest_digest,
            "outputs": [output_rel],
            "output_hashes": {output_rel: sha256_file(path / output_rel)},
            "warnings": [] if qc["status"] == "pass" else ["privacy or data review required"],
            "errors": [],
            "duration_seconds": round(time.perf_counter() - started, 6),
            "status": qc["status"],
        }
        write_json(path / "provenance" / "runs" / f"{run_id}.json", run)
        return {"ok": True, "command": "qc", "project_id": project_id, "run_id": run_id, "manifest": manifest, "qc": qc}

    def command_provenance(self, project_id: str) -> dict[str, Any]:
        path = self.project_path(project_id)
        manifest_path = path / "data" / "manifests" / "raw-manifest.json"
        manifest = load_text_record(manifest_path, None)
        verification = self._verify_manifest(path, manifest) if isinstance(manifest, dict) else {"valid": False, "reason": "manifest missing"}
        runs = []
        runs_path = path / "provenance" / "runs"
        if runs_path.is_dir():
            for run_path in sorted(runs_path.glob("*.json")):
                record = load_text_record(run_path, {})
                if isinstance(record, dict):
                    runs.append(record)
        return {"ok": True, "command": "provenance show", "project_id": project_id, "manifest": manifest or {}, "verification": verification, "runs": runs}

    def command_reproduce(self, run_id: str, project_id: str | None = None) -> dict[str, Any]:
        matches: list[tuple[Path, dict[str, Any]]] = []
        roots = [self.project_path(project_id)] if project_id else [Path(record["path"]) for record in self.project_records()]
        for root in roots:
            run_dir = root / "provenance" / "runs"
            if not run_dir.is_dir():
                continue
            for run_path in run_dir.glob("*.json"):
                if run_path.stem == run_id or run_path.stem.startswith(run_id):
                    record = load_text_record(run_path, {})
                    if isinstance(record, dict):
                        matches.append((root, record))
        if len(matches) != 1:
            raise ResearchCtlError("run id must resolve to exactly one recorded run")
        root, run = matches[0]
        manifest = load_text_record(root / str(run.get("input_manifest", "")), None)
        verification = self._verify_manifest(root, manifest) if isinstance(manifest, dict) else {"valid": False, "reason": "input manifest missing"}
        output_checks = []
        for relative, expected in (run.get("output_hashes") or {}).items():
            output_path = (root / str(relative)).resolve()
            inside = root.resolve() in output_path.parents
            exists = inside and output_path.is_file() and not output_path.is_symlink()
            actual = sha256_file(output_path) if exists else None
            output_checks.append({"path": relative, "exists": exists, "unchanged": exists and actual == expected})
        verification["outputs"] = output_checks
        verification["valid"] = bool(verification.get("valid")) and all(item["unchanged"] for item in output_checks)
        return {"ok": True, "command": "reproduce", "run_id": run.get("run_id"), "project_id": run.get("project_id"), "recorded_command": run.get("command"), "verification": verification, "reproducible": bool(verification.get("valid"))}

    def command_submission_preflight(self, project_path: str, manuscript: str | None = None, web_evidence: str | None = None) -> dict[str, Any]:
        root = Path(project_path).expanduser().resolve()
        if not root.is_dir():
            raise ResearchCtlError("project path is not a directory")
        project = load_text_record(root / "project.yaml", {}) or {}
        status_record = load_text_record(root / "status.yaml", {}) or {}
        project_id = str(project.get("project_id", root.name))
        manuscript_root = Path(manuscript).expanduser().resolve() if manuscript else root / "manuscript"
        if manuscript_root.is_file():
            manuscript_files = [manuscript_root]
        elif manuscript_root.is_dir():
            manuscript_files = sorted(item for item in manuscript_root.rglob("*") if item.is_file() and item.suffix.lower() in {".md", ".qmd", ".tex", ".doc", ".docx", ".txt"})
        else:
            manuscript_files = []

        checks: list[dict[str, Any]] = []
        checks.append({"name": "project_yaml", "status": "PASS" if (root / "project.yaml").is_file() else "FAIL", "detail": "project metadata present"})
        checks.append({"name": "status_yaml", "status": "PASS" if (root / "status.yaml").is_file() else "WARN", "detail": str(status_record.get("status", status_record.get("current_stage", "unknown")))})
        checks.append({"name": "manuscript_input", "status": "PASS" if manuscript_files else "BLOCKED", "detail": f"{len(manuscript_files)} manuscript source file(s)"})

        raw_manifest_path = root / "data" / "manifests" / "raw-manifest.json"
        raw_manifest = load_text_record(raw_manifest_path, None)
        manifest_check = self._verify_manifest(root, raw_manifest) if isinstance(raw_manifest, dict) else {"valid": False}
        if not manifest_check.get("valid") and isinstance(raw_manifest, dict) and isinstance(raw_manifest.get("files"), list):
            legacy_checks = []
            for entry in raw_manifest["files"]:
                relative = str(entry.get("path", ""))
                candidate = (root / relative).resolve()
                expected_hash = entry.get("sha256")
                inside = root.resolve() in candidate.parents
                exists = inside and candidate.is_file() and not candidate.is_symlink()
                legacy_checks.append(exists and sha256_file(candidate) == expected_hash)
            manifest_check = {"valid": bool(legacy_checks) and all(legacy_checks), "legacy_manifest": True}
        checks.append({"name": "raw_manifest_and_hashes", "status": "PASS" if manifest_check.get("valid") else "BLOCKED", "detail": "raw inputs unchanged" if manifest_check.get("valid") else "manifest missing or mismatch"})
        privacy = self._privacy_scan(root)
        privacy_status = "FAIL" if privacy.get("secret_file_count", 0) else ("WARN" if privacy.get("potential_phi_header_count", 0) or privacy.get("unreadable_file_count", 0) else "PASS")
        checks.append({"name": "privacy_and_raw_protection", "status": privacy_status, "detail": "counts only; no secret values emitted"})

        text = "\n".join(item.read_text(encoding="utf-8", errors="ignore")[:2_000_000] for item in manuscript_files if item.suffix.lower() not in {".doc", ".docx"})
        figures = sorted((root / "results" / "figures").glob("*") if (root / "results" / "figures").is_dir() else [])
        tables = sorted((root / "results" / "tables").glob("*") if (root / "results" / "tables").is_dir() else [])
        figure_refs = len(re.findall(r"(?i)\bfig(?:ure)?\s*\d+", text))
        table_refs = len(re.findall(r"(?i)\btable\s*\d+", text))
        checks.append({"name": "figure_table_inventory", "status": "PASS" if (figures or tables) and (figure_refs or table_refs) else "WARN", "detail": f"files={len(figures)} figures/{len(tables)} tables; references={figure_refs} figure/{table_refs} table"})
        doi_count = len(set(re.findall(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", text, flags=re.I)))
        pmid_count = len(set(re.findall(r"(?i)\bPMID\s*[:]?\s*\d+", text)))
        checks.append({"name": "citation_identifiers", "status": "PASS" if doi_count or pmid_count else ("BLOCKED" if manuscript_files else "WARN"), "detail": f"unique DOI={doi_count}; PMID={pmid_count}; identifier existence only"})

        template = str(project.get("type", project.get("template", ""))).lower()
        guideline = "PRISMA" if "systematic" in template or "meta" in template else "MIQE" if "qpcr" in template else "STROBE" if "clinical" in template or "observ" in template else "scRNA-seq methods + donor-unit rule" if "scrna" in template or "single" in template else "domain-specific reporting checklist"
        guideline_present = guideline.split()[0].casefold() in text.casefold() if text else False
        checks.append({"name": "reporting_guideline", "status": "PASS" if guideline_present else "WARN", "detail": guideline})
        checks.append({"name": "numeric_consistency", "status": "WARN" if manuscript_files else "BLOCKED", "detail": "manual cross-check required for n, effect, CI, P, tables and figures"})

        web_status = "BLOCKED"
        web_detail = "no web evidence file supplied"
        if web_evidence:
            evidence_path = Path(web_evidence).expanduser().resolve()
            evidence = load_text_record(evidence_path, None)
            sources = evidence.get("sources") if isinstance(evidence, dict) else None
            checked_at = evidence.get("checked_at") if isinstance(evidence, dict) else None
            web_status = "PASS" if isinstance(sources, list) and bool(sources) and checked_at else "BLOCKED"
            web_detail = f"sources={len(sources) if isinstance(sources, list) else 0}; checked_at={checked_at or 'missing'}"
        checks.append({"name": "journal_instructions_and_retractions", "status": web_status, "detail": web_detail})

        priority = {item["status"] for item in checks}
        if "FAIL" in priority:
            overall = "FAIL"
        elif "BLOCKED" in priority:
            overall = "BLOCKED"
        elif "WARN" in priority:
            overall = "WARN"
        else:
            overall = "PASS"
        report_path = root / "reports" / "SUBMISSION_PREFLIGHT_REPORT.md"
        report_lines = [f"# Submission Preflight — {project_id}", "", f"Generated: {utc_now()}", f"Overall: **{overall}**", "", "This is a gate report; it does not promote a manuscript or alter protected research decisions.", "", "| Check | Status | Detail |", "|---|---|---|"]
        report_lines.extend(f"| {item['name']} | {item['status']} | {item['detail']} |" for item in checks)
        report_lines.extend(["", "## Required human review", "", "- Verify every numeric claim against source tables and figures.", "- Verify DOI/PMID resolution, retractions, reporting guideline, journal instructions and supplement requirements using current authoritative web sources.", "- Confirm privacy clearance and that no raw/restricted data are uploaded."])
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
        return {"ok": True, "command": "submission preflight", "project_id": project_id, "project_path": str(root), "overall_status": overall, "checks": checks, "report": str(report_path)}

    def command_review(self, cadence: str) -> dict[str, Any]:
        if cadence not in {"weekly", "monthly"}:
            raise ResearchCtlError("review cadence must be weekly or monthly")
        records = self.project_records()
        return {"ok": True, "command": "review", "cadence": cadence, "mode": "review_only", "projects_checked": len(records), "changes": [], "privacy": "no project contents emitted"}

    def command_optimize_check(self) -> dict[str, Any]:
        policy = load_text_record(self.root / "config" / "optimization-policy.yaml", {}) or {}
        protected = load_text_record(self.root / "config" / "protected-core.yaml", {}) or {}
        return {"ok": True, "command": "optimize --check", "mode": "review_only", "eligible_for_auto_change": False, "priority": policy.get("priority", []), "protected_core": sorted((protected.get("protected") or {}).keys()), "changes": []}

    def command_registry_rebuild(self) -> dict[str, Any]:
        records = self.project_records()
        target = self.root / "registry" / "PROJECT_REGISTRY.csv"
        target.parent.mkdir(parents=True, exist_ok=True)
        fields = ["id", "title", "template", "privacy_level", "status", "path"]
        temporary = target.with_name(target.name + ".tmp")
        with temporary.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows({field: record.get(field, "") for field in fields} for record in records)
        os.replace(temporary, target)
        return {"ok": True, "command": "registry rebuild", "path": str(target), "count": len(records), "source_of_truth": "project.yaml and status.yaml"}


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="researchctl", description="Deterministic research project control plane")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    skills = sub.add_parser("skills")
    skills_sub = skills.add_subparsers(dest="skills_command", required=True)
    skills_sub.add_parser("audit")
    sub.add_parser("projects")
    new = sub.add_parser("new")
    new.add_argument("--template", required=True)
    new.add_argument("--id", required=True, dest="project_id")
    new.add_argument("--title", required=True)
    status = sub.add_parser("status")
    status.add_argument("project_id")
    status.add_argument("--set", dest="new_status")
    status.add_argument("--status", dest="new_status_alias")
    status.add_argument("--reason")
    route = sub.add_parser("route")
    route.add_argument("query", nargs="+")
    sub.add_parser("qc").add_argument("project_id")
    provenance = sub.add_parser("provenance")
    provenance_sub = provenance.add_subparsers(dest="provenance_command", required=True)
    provenance_sub.add_parser("show").add_argument("project_id")
    reproduce = sub.add_parser("reproduce")
    reproduce.add_argument("run_id")
    reproduce.add_argument("--project", dest="project_id")
    submission = sub.add_parser("submission")
    submission_sub = submission.add_subparsers(dest="submission_command", required=True)
    preflight = submission_sub.add_parser("preflight")
    preflight.add_argument("--path", required=True, dest="project_path")
    preflight.add_argument("--manuscript")
    preflight.add_argument("--web-evidence")
    review = sub.add_parser("review")
    review.add_argument("cadence", nargs="?", default="weekly")
    optimize = sub.add_parser("optimize")
    optimize.add_argument("--check", action="store_true")
    registry = sub.add_parser("registry")
    registry_sub = registry.add_subparsers(dest="registry_command", required=True)
    registry_sub.add_parser("rebuild")
    return parser


def dispatch(args: argparse.Namespace, ctl: ResearchCtl) -> dict[str, Any]:
    if args.command == "doctor":
        return ctl.command_doctor()
    if args.command == "skills" and args.skills_command == "audit":
        return ctl.command_skills_audit()
    if args.command == "projects":
        return ctl.command_projects()
    if args.command == "new":
        return ctl.command_new(args.template, args.project_id, args.title)
    if args.command == "status":
        return ctl.command_status(args.project_id, args.new_status or args.new_status_alias, args.reason)
    if args.command == "route":
        return ctl.command_route(" ".join(args.query))
    if args.command == "qc":
        return ctl.command_qc(args.project_id)
    if args.command == "provenance" and args.provenance_command == "show":
        return ctl.command_provenance(args.project_id)
    if args.command == "reproduce":
        return ctl.command_reproduce(args.run_id, args.project_id)
    if args.command == "submission" and args.submission_command == "preflight":
        return ctl.command_submission_preflight(args.project_path, args.manuscript, args.web_evidence)
    if args.command == "review":
        return ctl.command_review(args.cadence)
    if args.command == "optimize":
        if not args.check:
            raise ResearchCtlError("optimize currently supports --check only")
        return ctl.command_optimize_check()
    if args.command == "registry" and args.registry_command == "rebuild":
        return ctl.command_registry_rebuild()
    raise ResearchCtlError("unsupported command")


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in raw or "-j" in raw
    raw = [item for item in raw if item not in {"--json", "-j"}]
    try:
        args = make_parser().parse_args(raw)
        result = dispatch(args, ResearchCtl())
        if as_json:
            print(json.dumps(scrub(result), ensure_ascii=False, sort_keys=True))
        else:
            print_human(result)
        return 0 if result.get("ok", False) else 1
    except (ResearchCtlError, OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"ok": False, "error": str(exc)}
        if as_json:
            print(json.dumps(scrub(result), ensure_ascii=False, sort_keys=True))
        else:
            print(f"ERROR: {result['error']}", file=sys.stderr)
        return 2


def print_human(result: dict[str, Any]) -> None:
    if result.get("ok"):
        command = result.get("command", "researchctl")
        print(f"{command}: PASS")
        for key in ("count", "status", "run_id", "primary_skill", "path", "reproducible"):
            if key in result:
                print(f"{key}: {result[key]}")
    else:
        print(f"ERROR: {result.get('error', 'failed')}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
