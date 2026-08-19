"""Read-only checks for capabilities that require user-owned local tooling."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any, Callable, Mapping


def _zotero_status(env: Mapping[str, str]) -> dict[str, Any]:
    export_path = env.get("ZOTERO_LIBRARY_JSON")
    if export_path and Path(export_path).is_file():
        return {
            "status": "READY_LOCAL_EXPORT",
            "path": export_path,
            "write_mode": "READ_ONLY_EXPORT",
            "next_user_action": "verify the export is metadata-only and use the local adapter; no library write is performed",
        }
    return {
        "status": "READ_FIRST_UNVERIFIED",
        "path": export_path,
        "write_mode": "NOT_CONNECTED",
        "next_user_action": "export Zotero JSON locally, set ZOTERO_LIBRARY_JSON for the command, then run the adapter health check",
    }


def _tool_status(command: str, *, name: str, env_name: str, env: Mapping[str, str], which_fn: Callable[[str], str | None]) -> dict[str, Any]:
    configured = env.get(env_name)
    if configured:
        return {
            "status": "CONFIGURED_PATH_UNVERIFIED",
            "command": command,
            "path": configured,
            "next_user_action": f"run the {name} contract and local-PDF smoke test using the configured path before formal use",
        }
    resolved = which_fn(command)
    if resolved:
        return {
            "status": "READY_LOCAL_TOOL",
            "command": command,
            "path": resolved,
            "next_user_action": f"run the {name} contract and local-PDF smoke test before using it in a formal review",
        }
    return {
        "status": "OPTIONAL_UNVERIFIED",
        "command": command,
        "path": None,
        "next_user_action": f"install and validate {name} in an isolated environment only if the review needs it; keep private PDFs local",
    }


def inspect_downstream(*, env: Mapping[str, str] | None = None, which_fn: Callable[[str], str | None] | None = None) -> dict[str, Any]:
    environment = os.environ if env is None else env
    resolver = shutil.which if which_fn is None else which_fn
    return {
        "zotero": _zotero_status(environment),
        "mineru": _tool_status("mineru", name="MinerU", env_name="MEDLIT_MINERU_BIN", env=environment, which_fn=resolver),
        "paperqa2": _tool_status("paperqa", name="PaperQA2", env_name="MEDLIT_PAPERQA_BIN", env=environment, which_fn=resolver),
        "policy": {
            "allow_cloud_fulltext": False,
            "upload_private_pdfs": False,
            "library_write": False,
        },
    }
