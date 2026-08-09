import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class PublicReleaseToolTests(unittest.TestCase):
    def run_json(self, script: str, *args: str):
        output = subprocess.check_output([sys.executable, str(ROOT / script), *args, "--json"], cwd=ROOT, text=True)
        return json.loads(output)

    def test_bootstrap_dry_run_is_non_installing(self):
        result = self.run_json("scripts/bootstrap.py", "--dry-run")
        self.assertTrue(result["ok"])
        self.assertEqual(result["installations"], [])
        self.assertEqual(result["uploads"], [])
        self.assertEqual(result["overwrites"], [])

    def test_public_audit_has_no_sensitive_matches(self):
        result = self.run_json("scripts/public_release_audit.py")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["secret_matches"], 0)
        self.assertEqual(result["private_path_matches"], 0)
        self.assertEqual(result["phi_pii_matches"], 0)


if __name__ == "__main__":
    unittest.main()
