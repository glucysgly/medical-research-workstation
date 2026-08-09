import csv
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import obsidian_adapter  # noqa: E402
import qpcr_qc  # noqa: E402
import zotero_adapter  # noqa: E402


class AdapterAndQpcrTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def _json_cli(self, module, args):
        output = StringIO()
        with redirect_stdout(output):
            code = module.main([*args, "--json"])
        return code, json.loads(output.getvalue())

    def test_zotero_health_reports_not_configured_without_reading_real_library(self):
        missing = self.root / "does-not-exist.json"
        code, result = self._json_cli(zotero_adapter, ["health", "--library-json", str(missing)])
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "not_configured")
        self.assertFalse(result["configured"])
        self.assertEqual(result["path"], str(missing.resolve()))

    def test_zotero_metadata_is_allowlisted_and_excludes_full_text_and_secrets(self):
        library = self.root / "library.json"
        library.write_text(
            json.dumps(
                {
                    "items": [
                        {
                            "key": "ABC123",
                            "title": "A safe title",
                            "creators": [{"firstName": "Ada", "lastName": "Lovelace"}],
                            "date": "2025",
                            "DOI": "10.1000/example",
                            "abstractNote": "private abstract",
                            "fullText": "private full text",
                            "api_key": "must-not-appear",
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        code, result = self._json_cli(
            zotero_adapter,
            ["get_metadata", "ABC123", "--library-json", str(library)],
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "ok")
        metadata = result["metadata"]
        self.assertEqual(metadata["title"], "A safe title")
        self.assertEqual(metadata["DOI"], "10.1000/example")
        self.assertNotIn("abstractNote", metadata)
        self.assertNotIn("fullText", metadata)
        self.assertNotIn("api_key", json.dumps(result))

    def test_obsidian_search_rejects_path_outside_explicit_vault(self):
        vault = self.root / "vault"
        vault.mkdir()
        outside = self.root / "outside.md"
        outside.write_text("# Outside\nneedle\n", encoding="utf-8")
        code, result = self._json_cli(
            obsidian_adapter,
            ["search", "needle", "--vault", str(vault), "--path", "../outside.md"],
        )
        self.assertEqual(code, 2)
        self.assertIn("outside vault", result["error"])

    def test_qpcr_counts_biological_replicates_not_technical_rows_and_reports_ct_anomalies(self):
        csv_path = self.root / "qpcr.csv"
        rows = [
            {"group": "control", "biological_replicate": "B1", "technical_replicate": "T1", "target": "GAPDH", "ct": "20"},
            {"group": "control", "biological_replicate": "B1", "technical_replicate": "T2", "target": "GAPDH", "ct": "21"},
            {"group": "control", "biological_replicate": "B2", "technical_replicate": "T1", "target": "GAPDH", "ct": "22"},
            {"group": "control", "biological_replicate": "B2", "technical_replicate": "T1", "target": "GAPDH", "ct": "23"},
            {"group": "treated", "biological_replicate": "B1", "technical_replicate": "T1", "target": "GAPDH", "ct": ""},
            {"group": "treated", "biological_replicate": "B2", "technical_replicate": "T1", "target": "GAPDH", "ct": "50"},
        ]
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

        report = qpcr_qc.review_csv(csv_path)
        self.assertEqual(report["biological_replicate_counts"], {"control": 2, "treated": 2})
        self.assertEqual(report["statistical_unit"], "biological_replicate")
        self.assertTrue(any(issue["type"] == "duplicate_technical_replicate" for issue in report["issues"]))
        self.assertTrue(any(issue["type"] == "missing_ct" for issue in report["issues"]))
        self.assertTrue(any(issue["type"] == "ct_out_of_range" for issue in report["issues"]))
        self.assertIn("technical_replicates_not_statistical_n", report["miqe_review_checklist"])


if __name__ == "__main__":
    unittest.main()
