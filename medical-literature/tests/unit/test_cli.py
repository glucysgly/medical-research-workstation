import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))

from medlit.cli import _emit, main  # noqa: E402
from medlit.domain.models import CanonicalPaper  # noqa: E402


class CliTests(unittest.TestCase):
    def test_json_emitter_is_safe_for_windows_gbk_stdout(self):
        buffer = io.BytesIO()
        stream = io.TextIOWrapper(buffer, encoding="gbk", errors="strict")
        try:
            with contextlib.redirect_stdout(stream):
                _emit({"title": "宫颈癌试验"}, as_json=True)
            stream.flush()
            payload = json.loads(buffer.getvalue().decode("ascii"))
        finally:
            stream.detach()
        self.assertEqual(payload["title"], "宫颈癌试验")

    def test_route_json_cli_exposes_mode_and_routes(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["route", "我要做正式系统综述", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["mode"], "FORMAL_REVIEW")
        self.assertIn("formal-literature-search", payload["routes"])

    def test_capabilities_json_cli_marks_commercial_databases_as_auth_required(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["capabilities", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["formal_search"]["embase"], "AUTH_REQUIRED")
        self.assertIn(payload["trial_registry"]["clinicaltrials"], {"READY", "READY_FALLBACK"})

    def test_capabilities_reflect_ncbi_configuration_without_exposing_key(self):
        output = io.StringIO()
        with patch.dict(os.environ, {"NCBI_EMAIL": "research@example.org", "NCBI_API_KEY": "secret-test-key"}, clear=False), contextlib.redirect_stdout(output):
            code = main(["capabilities", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["formal_search"]["pubmed"], "READY_FALLBACK")
        self.assertNotIn("secret-test-key", output.getvalue())

    def test_capabilities_reflect_isolated_fulltext_tools(self):
        output = io.StringIO()
        with patch.dict(os.environ, {"MEDLIT_MINERU_BIN": sys.executable, "MEDLIT_PAPERQA_BIN": sys.executable}, clear=False), contextlib.redirect_stdout(output):
            code = main(["capabilities", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["parser"]["mineru"], "READY_LOCAL_TOOL")
        self.assertEqual(payload["reader"]["paperqa2"], "READY_LOCAL_TOOL")

    def test_v2_cli_surface_exposes_pending_downstream_gates_honestly(self):
        for command in ["search", "formal-search", "challenge", "search-qa", "verify", "resolve", "ingest", "parse", "read", "screen", "extract", "rob", "synthesize", "audit", "freeze", "e2e"]:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main([command, "--json"])
            self.assertEqual(code, 0, command)
            payload = json.loads(output.getvalue())
            self.assertIn(payload["status"], {"AUTH_REQUIRED", "PENDING_INPUT", "PENDING_DOWNSTREAM_INTEGRATION", "SKIP", "GATES_REPORTED"}, command)

    def test_quick_search_uses_official_pubmed_fallback_when_email_is_configured(self):
        class FakePubMed:
            def __init__(self, *, email):
                self.email = email

            async def search(self, query, *, run_id):
                return [CanonicalPaper(paper_id="pmid:1", title=query, pmid="1")]

        output = io.StringIO()
        with patch.dict(os.environ, {"NCBI_EMAIL": "research@example.org"}, clear=False), patch("medlit.cli.PubMedEutilsAdapter", FakePubMed), contextlib.redirect_stdout(output):
            code = main(["search", "--query", "cervical cancer", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["status"], "READY_FALLBACK")
        self.assertEqual(payload["count"], 1)
        self.assertTrue(payload["run_id"].startswith("cli-search-"))

    def test_search_qa_consumes_provider_json_and_returns_metrics(self):
        formal = [{"pmid": "1", "title": "Formal paper", "year": 2024}]
        challenger = [
            {"pmid": "1", "title": "Formal paper", "year": 2024},
            {"doi": "10.1000/new", "title": "Challenger paper", "year": 2023},
        ]
        with tempfile.TemporaryDirectory() as temp:
            formal_path = Path(temp) / "formal.json"
            challenger_path = Path(temp) / "challenger.json"
            formal_path.write_text(json.dumps(formal), encoding="utf-8")
            challenger_path.write_text(json.dumps(challenger), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main(["search-qa", "--formal-json", str(formal_path), "--challenger-json", str(challenger_path), "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["status"], "READY")
        self.assertEqual(payload["qa"]["challenger_unique"], ["doi:10.1000/new"])
        self.assertIn("source_overlap", payload)

    def test_verify_consumes_provider_json(self):
        record = {
            "title": "A controlled trial",
            "doi": "10.1000/abc",
            "year": 2024,
            "authors": ["A. Author"],
            "provider_records": {
                "crossref": {"doi": "10.1000/abc", "title": "A controlled trial", "year": 2024},
                "pubmed": {"doi": "10.1000/abc", "title": "A controlled trial", "year": 2024},
            },
        }
        with tempfile.TemporaryDirectory() as temp:
            input_path = Path(temp) / "citation.json"
            input_path.write_text(json.dumps(record), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main(["verify", "--input", str(input_path), "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["verification"]["state"], "VERIFIED_HIGH")

    def test_freeze_writes_readable_manifest_with_digest(self):
        request = {
            "freeze_id": "freeze-test",
            "databases": {"pubmed": {"query": "cervical cancer", "count": 12}},
            "dedup_count": 10,
            "citation_snowball_count": 3,
            "challenger_unique_reviewed": 1,
            "known_item_recall": 0.8,
            "reviewer": "test",
        }
        with tempfile.TemporaryDirectory() as temp:
            input_path = Path(temp) / "freeze.json"
            output_path = Path(temp) / "SEARCH_FREEZE_MANIFEST.yaml"
            input_path.write_text(json.dumps(request), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main(["freeze", "--input", str(input_path), "--output", str(output_path), "--json"])
            payload = json.loads(output.getvalue())
            saved = json.loads(payload["manifest_json"])
            self.assertTrue(output_path.exists())
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "READY")
        self.assertEqual(saved["freeze_id"], "freeze-test")
        self.assertEqual(len(saved["sha256"]), 64)

    def test_offline_e2e_command_runs_core_pipeline(self):
        with tempfile.TemporaryDirectory() as temp:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main(["e2e", "--output-root", temp, "--json"])
            payload = json.loads(output.getvalue())
            self.assertTrue(Path(payload["run_dir"]).exists())
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "PASS_OFFLINE_CORE")

    def test_upstream_check_reports_locked_components_without_faking_live_audit(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["upstream", "check", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["status"], "LOCKED_UNVERIFIED")
        self.assertTrue(payload["providers"])
        self.assertTrue(all("locked_sha" in provider for provider in payload["providers"]))


if __name__ == "__main__":
    unittest.main()
