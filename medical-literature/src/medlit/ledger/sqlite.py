from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA_VERSION = 1
TABLES = {
    "projects": "project_id TEXT PRIMARY KEY, title TEXT NOT NULL, created_at TEXT NOT NULL",
    "search_runs": "run_id TEXT PRIMARY KEY, run_type TEXT NOT NULL, query TEXT, created_at TEXT NOT NULL",
    "search_queries": "query_id INTEGER PRIMARY KEY, run_id TEXT NOT NULL, database_name TEXT NOT NULL, query TEXT NOT NULL",
    "raw_records": "record_id INTEGER PRIMARY KEY, run_id TEXT NOT NULL, provider TEXT NOT NULL, raw_json TEXT NOT NULL",
    "papers": "paper_id TEXT PRIMARY KEY, title TEXT NOT NULL, doi TEXT, pmid TEXT, pmcid TEXT, payload_json TEXT NOT NULL",
    "paper_sources": "source_id INTEGER PRIMARY KEY, paper_id TEXT NOT NULL, source TEXT NOT NULL, source_role TEXT NOT NULL, run_id TEXT NOT NULL, payload_json TEXT NOT NULL",
    "citation_edges": "edge_id TEXT PRIMARY KEY, source_paper_id TEXT NOT NULL, target_paper_id TEXT NOT NULL, direction TEXT NOT NULL, provider TEXT NOT NULL, depth INTEGER NOT NULL, run_id TEXT NOT NULL",
    "clinical_trials": "trial_id TEXT PRIMARY KEY, registry TEXT NOT NULL, title TEXT NOT NULL, payload_json TEXT NOT NULL",
    "trial_publication_links": "link_id INTEGER PRIMARY KEY, trial_id TEXT NOT NULL, paper_id TEXT NOT NULL, link_type TEXT NOT NULL, source TEXT NOT NULL, confidence REAL, verified INTEGER NOT NULL",
    "verification_events": "event_id INTEGER PRIMARY KEY, paper_id TEXT NOT NULL, state TEXT NOT NULL, payload_json TEXT NOT NULL",
    "search_qa_runs": "qa_id INTEGER PRIMARY KEY, run_id TEXT NOT NULL, payload_json TEXT NOT NULL",
    "known_item_tests": "test_id INTEGER PRIMARY KEY, run_id TEXT NOT NULL, payload_json TEXT NOT NULL",
    "fulltext_assets": "asset_id INTEGER PRIMARY KEY, paper_id TEXT NOT NULL, path TEXT, status TEXT NOT NULL, payload_json TEXT NOT NULL",
    "zotero_links": "link_id INTEGER PRIMARY KEY, paper_id TEXT NOT NULL, zotero_key TEXT NOT NULL, payload_json TEXT NOT NULL",
    "screening_decisions": "decision_id INTEGER PRIMARY KEY, paper_id TEXT NOT NULL, stage TEXT NOT NULL, decision TEXT NOT NULL, payload_json TEXT NOT NULL",
    "analysis_artifacts": "artifact_id INTEGER PRIMARY KEY, run_id TEXT NOT NULL, path TEXT NOT NULL, sha256 TEXT NOT NULL",
    "evidence_items": "evidence_id INTEGER PRIMARY KEY, paper_id TEXT NOT NULL, payload_json TEXT NOT NULL",
    "rob_judgements": "judgement_id INTEGER PRIMARY KEY, paper_id TEXT NOT NULL, payload_json TEXT NOT NULL",
    "audit_events": "event_id INTEGER PRIMARY KEY, event_type TEXT NOT NULL, payload_json TEXT NOT NULL",
}


class LiteratureLedger:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def ensure_schema(self) -> int:
        connection = self._connect()
        try:
            connection.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY)")
            for name, columns in TABLES.items():
                connection.execute(f"CREATE TABLE IF NOT EXISTS {name} ({columns})")
            connection.execute("INSERT OR IGNORE INTO schema_migrations(version) VALUES (?)", (SCHEMA_VERSION,))
            connection.commit()
        finally:
            connection.close()
        return SCHEMA_VERSION

    def table_names(self) -> list[str]:
        connection = self._connect()
        try:
            rows = connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()
        finally:
            connection.close()
        return [row[0] for row in rows]
