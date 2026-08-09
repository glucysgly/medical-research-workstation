import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
import researchctl  # noqa: E402


class ResearchCtlUnitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "config").mkdir()
        (self.root / "templates" / "synthetic").mkdir(parents=True)
        (self.root / "README.md").write_text("fixture\n", encoding="utf-8")
        (self.root / "AGENTS.md").write_text("fixture\n", encoding="utf-8")
        (self.root / "config" / "workstation.yaml").write_text(
            "schema_version: 1\nworkstation:\n  raw_data_immutable: true\n", encoding="utf-8"
        )
        (self.root / "config" / "skill-index.yaml").write_text(
            "schema_version: 1\nskills:\n  - name: data-qc\n    category: data\n    triggers: [QC]\n", encoding="utf-8"
        )
        self.ctl = researchctl.ResearchCtl(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_route_is_deterministic_and_scrub_keeps_policy_flag(self):
        result = self.ctl.command_route("check missing values in qPCR data")
        self.assertEqual(result["primary_skill"], "data-analytics:validate-data")
        self.assertEqual(result["task_code"], "BIO")
        clean = researchctl.scrub({"secret_output": False, "token": "do-not-print"})
        self.assertFalse(clean["secret_output"])
        self.assertEqual(clean["token"], "[REDACTED]")

    def test_status_change_requires_reason_and_records_history(self):
        self.ctl.command_new("synthetic", "study-1", "Synthetic study")
        with self.assertRaises(researchctl.ResearchCtlError):
            self.ctl.command_status("study-1", "active", None)
        result = self.ctl.command_status("study-1", "active", "start fixture work")
        self.assertEqual(result["status"], "active")
        self.assertEqual(result["status_history"][-1]["reason"], "start fixture work")


if __name__ == "__main__":
    unittest.main()
