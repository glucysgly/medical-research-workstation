import sys
import unittest
from pathlib import Path


SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))

from medlit.rate_limit import RateLimitManager  # noqa: E402
from medlit.search_qa.metrics import build_freeze_manifest, compute_metrics  # noqa: E402


class SearchControlTests(unittest.TestCase):
    def test_rate_limit_manager_tracks_provider_configuration(self):
        manager = RateLimitManager({"semantic-scholar": {"requests_per_second": 2, "max_retries": 3}})
        self.assertEqual(manager.policy("semantic-scholar")["max_retries"], 3)
        self.assertEqual(manager.policy("missing")["max_retries"], 0)

    def test_metrics_and_freeze_manifest_keep_challenger_out_of_prisma_count(self):
        metrics = compute_metrics(
            formal_count=10,
            challenger_intersection=8,
            challenger_unique=2,
            verified_count=9,
            unresolved_doi=1,
            dedup_review=1,
            trial_links=3,
            trials=4,
            citation_unique=5,
            citation_total=20,
        )
        self.assertEqual(metrics["formal_challenger_overlap"], 0.8)
        self.assertEqual(metrics["unresolved_doi_rate"], 0.1)
        manifest = build_freeze_manifest(
            freeze_id="freeze-1",
            databases={"pubmed": {"query": "x", "count": 10}},
            dedup_count=10,
            citation_snowball_count=5,
            challenger_unique_reviewed=2,
            known_item_recall=1.0,
            reviewer="human",
        )
        self.assertEqual(manifest["result_counts"]["pubmed"], 10)
        self.assertNotIn("challenger_unique", manifest["result_counts"])
        self.assertIsNotNone(manifest["date"])
        self.assertEqual(len(manifest["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
