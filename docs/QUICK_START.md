# Quick start

1. Copy one directory from `templates/` into a project location.
2. Fill `project.yaml` and `status.yaml`; keep `privacy_level: restricted` unless
   access is explicitly verified.
3. Complete `protocol/README.md`, add literature search/source records, and ingest
   immutable raw data with a SHA-256 manifest.
4. Select the matching `domain-packs/*/routing-contract.md` and catalog row.
5. Run only after protected fields are resolved; write derived data/results and
   `provenance/run-manifest.yaml`.
6. QA outputs, update status, and record limitations in retrospective.

Deterministic entry points:

~~~powershell
.\bin\researchctl.cmd doctor --json
.\bin\researchctl.cmd route "检查 qPCR 数据缺失和重复" --json
python scripts\qpcr_qc.py --input path\to\qpcr.csv --json
python scripts\zotero_adapter.py health --json
python scripts\obsidian_adapter.py health --json
~~~
