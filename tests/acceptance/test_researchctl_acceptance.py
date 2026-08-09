import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = PROJECT_ROOT / "scripts" / "researchctl.py"


class ResearchCtlAcceptanceTests(unittest.TestCase):
    def test_json_cli_contract_for_new_project_and_status(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "config").mkdir()
            (root / "templates" / "clinical-study").mkdir(parents=True)
            (root / "README.md").write_text("fixture\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("fixture\n", encoding="utf-8")
            (root / "config" / "workstation.yaml").write_text("schema_version: 1\n", encoding="utf-8")
            environment = dict(os.environ, RESEARCHCTL_ROOT=str(root))
            command = [sys.executable, str(SCRIPT), "new", "--template", "clinical-study", "--id", "acceptance-1", "--title", "Synthetic", "--json"]
            created = subprocess.run(command, capture_output=True, text=True, env=environment, check=False)
            self.assertEqual(created.returncode, 0, created.stderr)
            payload = json.loads(created.stdout)
            self.assertTrue(payload["ok"])
            status = subprocess.run([sys.executable, str(SCRIPT), "status", "acceptance-1", "--json"], capture_output=True, text=True, env=environment, check=False)
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertEqual(json.loads(status.stdout)["status"], "IDEA")


if __name__ == "__main__":
    unittest.main()
