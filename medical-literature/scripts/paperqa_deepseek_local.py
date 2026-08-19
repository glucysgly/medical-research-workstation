"""Run deterministic local PaperQA2 evidence QA with a DeepSeek-compatible LLM.

This path uses Docs.aquery instead of the PaperQA agent ToolSelector. The
installed PaperQA2 build currently has a dependency mismatch in that agent
layer, while the direct document/evidence/query API is working.
"""

from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path

from paperqa import Docs, Settings


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SETTINGS = PROJECT_ROOT / "config" / "paperqa.deepseek.example.json"
SUPPORTED_SUFFIXES = {".pdf", ".md", ".txt", ".html", ".htm"}


def collect_inputs(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(
            candidate
            for candidate in path.rglob("*")
            if candidate.is_file() and candidate.suffix.lower() in SUPPORTED_SUFFIXES
        )
    raise FileNotFoundError(path)


async def run(input_path: Path, question: str, settings_path: Path) -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY must be set for the current process; map it from "
            "DEEPSEEK_API_KEY without storing the key in this repository."
        )
    settings = Settings.model_validate_json(settings_path.read_text(encoding="utf-8"))
    inputs = collect_inputs(input_path)
    if not inputs:
        raise RuntimeError(f"No supported documents found under {input_path}")

    docs = Docs()
    names: list[str] = []
    for document in inputs:
        name = await docs.aadd(document, settings=settings)
        if name:
            names.append(name)
    session = await docs.aquery(question, settings=settings)

    print(f"PAPERQA_DOCUMENTS={len(names)}")
    print(f"PAPERQA_CONTEXTS={len(session.contexts)}")
    print("PAPERQA_ANSWER_START")
    print(session.answer)
    print("PAPERQA_ANSWER_END")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="One local PDF or a document directory")
    parser.add_argument("--question", required=True, help="Question to answer from the supplied documents")
    parser.add_argument("--settings", type=Path, default=DEFAULT_SETTINGS)
    args = parser.parse_args()
    return asyncio.run(run(args.input, args.question, args.settings))


if __name__ == "__main__":
    raise SystemExit(main())
