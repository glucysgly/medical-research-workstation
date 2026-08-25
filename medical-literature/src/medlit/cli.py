from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from medlit.adapters.citation.semantic_scholar import SemanticScholarCitationAdapter
from medlit.adapters.search.pubmed import PubMedEutilsAdapter
from medlit.adapters.trials.clinicaltrials_official import OfficialClinicalTrialsAdapter
from medlit.artifacts import freeze_from_json, offline_e2e, search_qa_from_json, verify_from_json
from medlit.downstream import inspect_downstream
from medlit.router.rules import route_query
from medlit.search_strategy.engine import lint_query
from medlit.upstream import check_locked_upstreams


def capabilities() -> dict[str, Any]:
    pubmed_ready = bool(os.environ.get("NCBI_EMAIL") and "@" in os.environ["NCBI_EMAIL"])
    mineru_ready = bool(os.environ.get("MEDLIT_MINERU_BIN") and Path(os.environ["MEDLIT_MINERU_BIN"]).is_file())
    paperqa_ready = bool(os.environ.get("MEDLIT_PAPERQA_BIN") and Path(os.environ["MEDLIT_PAPERQA_BIN"]).is_file())
    return {
        "formal_search": {
            "pubmed": "READY_FALLBACK" if pubmed_ready else "AUTH_REQUIRED",
            "embase": "AUTH_REQUIRED",
            "wos": "AUTH_REQUIRED",
            "scopus": "AUTH_REQUIRED",
            "cnki": "MANUAL_REQUIRED",
            "central": "MANUAL_REQUIRED",
        },
        "discovery": {"paper_search": "UNVERIFIED"},
        "trial_registry": {
            "clinicaltrials": "READY_FALLBACK",
            "isrctn": "OPTIONAL_UNVERIFIED",
            "who_ictrp": "EXPERIMENTAL",
        },
        "citation": {"semantic_scholar": "READY_FALLBACK", "openalex_crosscheck": "OPTIONAL_UNVERIFIED"},
        "qa": {"doi_verifier": "READY_FALLBACK", "challenger": "OPTIONAL_UNVERIFIED"},
        "library": {"zotero": "READ_FIRST_UNVERIFIED"},
        "parser": {"mineru": "READY_LOCAL_TOOL" if mineru_ready else "OPTIONAL_UNVERIFIED"},
        "reader": {"paperqa2": "READY_LOCAL_TOOL" if paperqa_ready else "OPTIONAL_UNVERIFIED"},
        "policy": {"allow_cloud_fulltext": False, "formal_counts_include_challenger": False},
    }


def doctor() -> dict[str, Any]:
    checks: dict[str, str] = {}
    for name in ("git", "python", "uv", "node", "npm"):
        checks[name] = "PASS" if shutil.which(name) else "FAIL"
    checks["sqlite"] = "PASS" if sqlite3.sqlite_version else "FAIL"
    checks["zotero"] = "MANUAL_REQUIRED"
    checks["codex_mcp"] = "MANUAL_REQUIRED"
    checks["ncbi_email"] = "PASS" if os.environ.get("NCBI_EMAIL") and "@" in os.environ["NCBI_EMAIL"] else "AUTH_REQUIRED"
    checks["ncbi_api_key"] = "CONFIGURED" if (os.environ.get("NCBI_API_KEY") or os.environ.get("NCBI_EUTILS_API_KEY")) else "OPTIONAL_NOT_SET"
    checks["network"] = "NOT_PROBED"
    overall = "FAIL" if "FAIL" in checks.values() else "PASS"
    return {"status": overall, "checks": checks, "capabilities": capabilities()}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="medlit", description="Medical literature research orchestrator V2")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    sub.add_parser("capabilities")
    route = sub.add_parser("route")
    route.add_argument("query", nargs="+")
    strategy = sub.add_parser("strategy")
    strategy.add_argument("--query", required=True)
    strategy.add_argument("--database", default="pubmed")
    trace = sub.add_parser("trace")
    trace.add_argument("paper_id")
    trace.add_argument("--run-id", required=True)
    trace.add_argument("--direction", choices=("references", "citations", "related"), default="references")
    trials = sub.add_parser("trials")
    trials.add_argument("--query")
    trials.add_argument("--id", dest="trial_id")
    search = sub.add_parser("search")
    search.add_argument("--query")
    formal = sub.add_parser("formal-search")
    formal.add_argument("--query")
    challenge = sub.add_parser("challenge")
    challenge.add_argument("--query")
    search_qa = sub.add_parser("search-qa")
    search_qa.add_argument("--formal-json")
    search_qa.add_argument("--challenger-json")
    search_qa.add_argument("--output")
    verify = sub.add_parser("verify")
    verify.add_argument("--input")
    freeze = sub.add_parser("freeze")
    freeze.add_argument("--input")
    freeze.add_argument("--output", default="SEARCH_FREEZE_MANIFEST.yaml")
    for name in ("resolve", "ingest", "parse", "read", "screen", "extract", "rob", "synthesize", "audit"):
        sub.add_parser(name)
    e2e = sub.add_parser("e2e")
    e2e.add_argument("--output-root")
    upstream = sub.add_parser("upstream")
    upstream_sub = upstream.add_subparsers(dest="upstream_command", required=True)
    upstream_sub.add_parser("check")
    return parser


def _emit(value: Any, as_json: bool) -> None:
    # Windows PowerShell may expose a GBK stdout stream. Escaping non-ASCII at
    # the terminal boundary keeps JSON machine-readable without changing the
    # UTF-8 encoding used for persisted artifacts.
    if as_json:
        print(json.dumps(value, ensure_ascii=True, sort_keys=True))
    elif isinstance(value, dict):
        print(json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True))
    else:
        print(value)


def _run_id(prefix: str) -> str:
    return f"{prefix}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in raw or "-j" in raw
    raw = [item for item in raw if item not in {"--json", "-j"}]
    try:
        args = _parser().parse_args(raw)
        if args.command == "doctor":
            result = doctor()
        elif args.command == "capabilities":
            result = capabilities()
        elif args.command == "route":
            result = route_query(" ".join(args.query))
        elif args.command == "strategy":
            result = lint_query(args.query, database=args.database)
        elif args.command == "trace":
            adapter = SemanticScholarCitationAdapter()
            if args.direction == "references":
                edges = asyncio.run(adapter.references(args.paper_id, run_id=args.run_id))
            elif args.direction == "citations":
                edges = asyncio.run(adapter.citations(args.paper_id, run_id=args.run_id))
            else:
                edges = asyncio.run(adapter.related(args.paper_id, run_id=args.run_id))
            result = {"status": "READY", "edges": [edge.__dict__ for edge in edges]}
        elif args.command == "trials":
            adapter = OfficialClinicalTrialsAdapter()
            if bool(args.query) == bool(args.trial_id):
                raise ValueError("provide exactly one of --query or --id")
            if args.query:
                records = asyncio.run(adapter.search(args.query))
            else:
                records = [asyncio.run(adapter.get_trial(args.trial_id))]
            result = {"status": "READY", "trials": [trial.to_dict() for trial in records]}
        elif args.command == "search":
            email = os.environ.get("NCBI_EMAIL")
            if not email:
                result = {"status": "AUTH_REQUIRED", "command": "search", "detail": "NCBI_EMAIL is required for the official PubMed fallback"}
            else:
                run_id = _run_id("cli-search")
                api_key = os.environ.get("NCBI_API_KEY") or os.environ.get("NCBI_EUTILS_API_KEY")
                adapter_kwargs = {"email": email}
                if api_key:
                    adapter_kwargs["api_key"] = api_key
                records = asyncio.run(PubMedEutilsAdapter(**adapter_kwargs).search(args.query or "", run_id=run_id))
                result = {"status": "READY_FALLBACK", "provider": "pubmed", "run_id": run_id, "count": len(records), "api_key_configured": bool(api_key), "records": [record.to_dict() for record in records]}
        elif args.command == "formal-search":
            result = {"status": "AUTH_REQUIRED", "command": args.command, "detail": "provider registration and/or formal database authorization is pending"}
        elif args.command == "challenge":
            result = {"status": "SKIP", "command": "challenge", "detail": "scholar-megasearch is optional and not configured"}
        elif args.command == "search-qa":
            if not args.formal_json or not args.challenger_json:
                result = {"status": "PENDING_INPUT", "command": args.command, "detail": "supply --formal-json and --challenger-json exports"}
            else:
                result = search_qa_from_json(args.formal_json, args.challenger_json)
                if args.output:
                    output_path = Path(args.output)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                    result["output"] = str(output_path)
        elif args.command == "verify":
            if not args.input:
                result = {"status": "PENDING_INPUT", "command": args.command, "detail": "supply --input citation JSON"}
            else:
                result = verify_from_json(args.input)
        elif args.command == "freeze":
            if not args.input:
                result = {"status": "PENDING_INPUT", "command": args.command, "detail": "supply --input freeze request JSON"}
            else:
                result = freeze_from_json(args.input, args.output)
        elif args.command == "audit":
            result = {"status": "GATES_REPORTED", "downstream": inspect_downstream()}
        elif args.command in {"resolve", "ingest", "parse", "read", "screen", "extract", "rob", "synthesize", "audit", "e2e"}:
            if args.command == "e2e" and args.output_root:
                result = offline_e2e(args.output_root)
            else:
                result = {"status": "PENDING_DOWNSTREAM_INTEGRATION", "command": args.command, "detail": "downstream provider or human review gate is not enabled"}
        elif args.command == "upstream" and args.upstream_command == "check":
            lock_path = Path(__file__).resolve().parents[2] / "config" / "upstreams.lock.yaml"
            result = check_locked_upstreams(lock_path)
        else:
            raise ValueError("unsupported command")
        _emit(result, as_json)
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        _emit({"status": "FAIL", "error": str(exc)}, as_json)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
