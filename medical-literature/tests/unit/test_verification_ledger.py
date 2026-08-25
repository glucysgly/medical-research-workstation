import asyncio
import sys
import tempfile
import unittest
from pathlib import Path


SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))

from medlit.adapters.verification.doi_fallback import evaluate_verification  # noqa: E402
from medlit.ledger.sqlite import LiteratureLedger  # noqa: E402


class VerificationLedgerTests(unittest.TestCase):
    def test_verification_requires_doi_and_two_authoritative_matches(self):
        high = evaluate_verification(
            title="A controlled trial",
            doi="10.1000/abc",
            year=2024,
            authors=["A. Author"],
            provider_records={
                "crossref": {"doi": "10.1000/abc", "title": "A controlled trial", "year": 2024, "authors": ["A. Author"]},
                "pubmed": {"doi": "10.1000/abc", "title": "A controlled trial", "year": 2024, "authors": ["A. Author"]},
            },
        )
        self.assertEqual(high.state, "VERIFIED_HIGH")

        conflict = evaluate_verification(
            title="A controlled trial",
            doi="10.1000/wrong",
            year=2024,
            authors=["A. Author"],
            provider_records={
                "crossref": {"doi": "10.1000/right", "title": "Different paper", "year": 2024, "authors": ["B. Author"]},
            },
        )
        self.assertEqual(conflict.state, "CONFLICT")

    def test_ledger_schema_migration_is_idempotent_and_preserves_tables(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "ledger.sqlite3"
            ledger = LiteratureLedger(path)
            first = ledger.ensure_schema()
            second = ledger.ensure_schema()
            tables = ledger.table_names()

        self.assertEqual(first, second)
        self.assertIn("papers", tables)
        self.assertIn("clinical_trials", tables)
        self.assertIn("citation_edges", tables)
        self.assertIn("search_qa_runs", tables)


if __name__ == "__main__":
    unittest.main()
