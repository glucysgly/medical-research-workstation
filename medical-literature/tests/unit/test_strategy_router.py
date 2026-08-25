import sys
import unittest
from pathlib import Path


SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))

from medlit.router.rules import route_query  # noqa: E402
from medlit.search_strategy.engine import known_item_recall, lint_query  # noqa: E402


class StrategyRouterTests(unittest.TestCase):
    def test_query_lint_flags_unbalanced_parentheses_and_date_limit(self):
        report = lint_query('(cervical cancer AND immunotherapy', database="pubmed")
        codes = {issue["code"] for issue in report["issues"]}
        self.assertIn("UNMATCHED_PARENTHESES", codes)

        report = lint_query('cervical cancer AND 2020:2024[dp]', database="pubmed")
        codes = {issue["code"] for issue in report["issues"]}
        self.assertIn("ACCIDENTAL_DATE_LIMIT", codes)

    def test_known_item_recall_requires_all_mandatory_items(self):
        report = known_item_recall(
            [
                {"id": "10.1000/one", "mandatory": True},
                {"id": "10.1000/two", "mandatory": True},
            ],
            [{"doi": "10.1000/one", "title": "One"}],
        )
        self.assertEqual(report["recall"], 0.5)
        self.assertEqual(report["status"], "SEARCH_STRATEGY_FAIL")
        self.assertEqual(report["missing_mandatory"], ["10.1000/two"])

    def test_known_item_recall_accepts_generator_inputs(self):
        items = ({"id": value, "mandatory": True} for value in ["10.1000/one", "10.1000/two"])
        report = known_item_recall(items, [{"doi": "10.1000/one", "title": "One"}])
        self.assertEqual(report["recall"], 0.5)

    def test_route_modes_are_deterministic_and_do_not_confuse_roles(self):
        self.assertEqual(route_query("我要做正式系统综述" )["mode"], "FORMAL_REVIEW")
        self.assertEqual(route_query("沿这篇文章找后续研究" )["mode"], "SEED_EXPANSION")
        self.assertEqual(route_query("有哪些正在招募的临床试验" )["mode"], "TRIAL_LANDSCAPE")
        self.assertEqual(route_query("找最近关于宫颈癌的研究" )["mode"], "QUICK")


if __name__ == "__main__":
    unittest.main()
