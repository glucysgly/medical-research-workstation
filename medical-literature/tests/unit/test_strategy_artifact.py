import sys
import unittest
from pathlib import Path


SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))

from medlit.search_strategy.artifact import build_query_artifact, render_yaml  # noqa: E402


class StrategyArtifactTests(unittest.TestCase):
    def test_query_artifact_supports_non_pico_framework_and_separate_queries(self):
        artifact = build_query_artifact(
            question="What is known about the process?",
            review_type="scoping",
            framework="PCC",
            concepts=[{"name": "Population", "controlled_terms": ["Term"], "free_terms": ["process"]}],
            databases=["pubmed", "cnki"],
            queries={"pubmed": "Term AND process", "cnki": "主题词 AND 过程"},
        )
        self.assertEqual(artifact["framework"], "PCC")
        self.assertEqual(artifact["queries"]["cnki"], "主题词 AND 过程")
        self.assertIn("framework: PCC", render_yaml(artifact))


if __name__ == "__main__":
    unittest.main()
