import sys
import tempfile
import unittest
from pathlib import Path


SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))

from medlit.orchestrator.offline import run_offline_pipeline  # noqa: E402


class OfflinePipelineTests(unittest.TestCase):
    def test_offline_pipeline_writes_provenance_and_qa_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            result = run_offline_pipeline(
                Path(temp),
                question="fixture question",
                formal_records=[{"title": "Shared", "doi": "10.1000/shared"}],
                discovery_records=[{"title": "Shared", "doi": "10.1000/shared"}, {"title": "Discovery", "doi": "10.1000/discovery"}],
                challenger_records=[{"title": "Shared", "doi": "10.1000/shared"}, {"title": "Gap", "doi": "10.1000/gap"}],
            )
            run_dir = Path(result["run_dir"])
            self.assertTrue((run_dir / "search_strategy.yaml").is_file())
            self.assertTrue((run_dir / "source_overlap.csv").is_file())
            self.assertTrue((run_dir / "search_qa.json").is_file())
            self.assertEqual(result["formal_count"], 1)
            self.assertEqual(result["challenger_unique_count"], 1)


if __name__ == "__main__":
    unittest.main()
