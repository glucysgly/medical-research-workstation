import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
import researchctl  # noqa: E402


class ManuscriptPipelineRouteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "config").mkdir()
        (self.root / "README.md").write_text("fixture\n", encoding="utf-8")
        (self.root / "AGENTS.md").write_text("fixture\n", encoding="utf-8")
        (self.root / "config" / "workstation.yaml").write_text(
            "schema_version: 1\nworkstation:\n  raw_data_immutable: true\n", encoding="utf-8"
        )
        self.ctl = researchctl.ResearchCtl(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_full_lifecycle_routes_to_pipeline(self):
        result = self.ctl.command_route("按阶段门控和三本账整理医学论文全流程")
        self.assertEqual(result["primary_skill"], "medical-manuscript-pipeline")
        self.assertEqual(result["workflow_key"], "medical-manuscript-pipeline")
        self.assertLessEqual(len(result["supporting_skills"]), 2)

    def test_single_systematic_review_keeps_specific_route(self):
        result = self.ctl.command_route("系统综述检索和PRISMA筛选")
        self.assertEqual(result["primary_skill"], "nature-academic-search")
        self.assertEqual(result["workflow_key"], "systematic")

    def test_single_manuscript_qc_keeps_specific_route(self):
        result = self.ctl.command_route("检查论文结果数字和图表")
        self.assertEqual(result["primary_skill"], "nature-reviewer")


if __name__ == "__main__":
    unittest.main()
