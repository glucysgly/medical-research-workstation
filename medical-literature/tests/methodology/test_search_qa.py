import sys
import unittest
from pathlib import Path


SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))

from medlit.canonical.normalize import normalize_paper  # noqa: E402
from medlit.domain.models import SourceRole  # noqa: E402
from medlit.search_qa.engine import compare_formal_challenger, source_overlap_matrix  # noqa: E402


def paper(title, doi, source, role):
    return normalize_paper(
        {"title": title, "doi": doi},
        source=source,
        source_role=role,
        run_id=f"run-{source}",
        query="fixture",
    )


class SearchQATests(unittest.TestCase):
    def test_challenger_unique_is_not_added_to_formal_count(self):
        formal = [paper("Shared", "10.1000/shared", "pubmed", SourceRole.FORMAL_DATABASE)]
        challenger = formal + [paper("Gap", "10.1000/gap", "challenger", SourceRole.CHALLENGER)]
        report = compare_formal_challenger(formal, challenger)
        self.assertEqual(report["formal_count"], 1)
        self.assertEqual(report["challenger_count"], 2)
        self.assertEqual(report["challenger_unique"], ["doi:10.1000/gap"])

    def test_overlap_matrix_contains_pairwise_intersections(self):
        one = paper("Shared", "10.1000/shared", "pubmed", SourceRole.FORMAL_DATABASE)
        two = paper("Only two", "10.1000/two", "paper-search", SourceRole.DISCOVERY_ENGINE)
        matrix = source_overlap_matrix({"pubmed": [one], "paper-search": [one, two]})
        self.assertEqual(matrix["rows"]["pubmed"]["paper-search"], 1)


if __name__ == "__main__":
    unittest.main()
