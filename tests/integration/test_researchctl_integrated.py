import hashlib
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
import researchctl  # noqa: E402


class ResearchCtlIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "config").mkdir()
        (self.root / "templates" / "qpcr-study").mkdir(parents=True)
        (self.root / "templates" / "qpcr-study" / "project.yaml").write_text(
            "schema_version: v5\nstudy_type: qpcr\nassay:\n  platform: VERIFY_REQUIRED\n",
            encoding="utf-8",
        )
        (self.root / "README.md").write_text("fixture\n", encoding="utf-8")
        (self.root / "AGENTS.md").write_text("fixture\n", encoding="utf-8")
        (self.root / "config" / "workstation.yaml").write_text("schema_version: 1\n", encoding="utf-8")
        self.ctl = researchctl.ResearchCtl(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_new_qc_provenance_and_reproduce_verify_hashes(self):
        created = self.ctl.command_new("qpcr-study", "synthetic-qpcr", "Synthetic qPCR")
        self.assertTrue(created["ok"])
        project = self.root / "projects" / "synthetic-qpcr"
        metadata = researchctl.load_text_record(project / "project.yaml", {})
        self.assertEqual(metadata["schema_version"], "v5")
        self.assertEqual(metadata["study_type"], "qpcr")
        status = self.ctl.command_status("synthetic-qpcr", "DATA_QC", "fixture intake passed")
        self.assertEqual(status["status"], "DATA_QC")
        raw = project / "data" / "raw" / "measurements.csv"
        raw.write_text("sample,ct\nA,20.1\nB,21.2\n", encoding="utf-8")
        before = hashlib.sha256(raw.read_bytes()).hexdigest()
        qc = self.ctl.command_qc("synthetic-qpcr")
        self.assertEqual(qc["qc"]["status"], "pass")
        self.assertEqual(before, hashlib.sha256(raw.read_bytes()).hexdigest())
        provenance = self.ctl.command_provenance("synthetic-qpcr")
        self.assertTrue(provenance["verification"]["valid"])
        replay = self.ctl.command_reproduce(qc["run_id"])
        self.assertTrue(replay["reproducible"])
        raw.write_text("sample,ct\nA,99.9\nB,21.2\n", encoding="utf-8")
        self.assertFalse(self.ctl.command_reproduce(qc["run_id"])["reproducible"])

    def test_registry_rebuild_uses_project_text_sources(self):
        self.ctl.command_new("qpcr-study", "registry-study", "Registry fixture")
        result = self.ctl.command_registry_rebuild()
        registry = self.root / "registry" / "PROJECT_REGISTRY.csv"
        self.assertTrue(result["ok"])
        self.assertTrue(registry.is_file())
        self.assertIn("registry-study", registry.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
