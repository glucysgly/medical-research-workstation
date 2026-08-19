import asyncio
import sys
import unittest
from pathlib import Path


SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))

from medlit.adapters.challenger.megasearch import ChallengerAdapter  # noqa: E402
from medlit.adapters.citation.semantic_scholar import SemanticScholarCitationAdapter  # noqa: E402


class AdapterTests(unittest.TestCase):
    def test_semantic_scholar_adapter_keeps_backward_and_forward_edges(self):
        def request_json(url):
            if url.endswith("/references"):
                return {"data": [{"citedPaper": {"paperId": "ref-1", "title": "Reference"}}]}
            if url.endswith("/citations"):
                return {"data": [{"citingPaper": {"paperId": "cite-1", "title": "Citing"}}]}
            return {"data": []}

        adapter = SemanticScholarCitationAdapter(request_json=request_json)
        references = asyncio.run(adapter.references("seed-1", run_id="run-1"))
        citations = asyncio.run(adapter.citations("seed-1", run_id="run-1"))
        self.assertEqual(references[0].direction, "CITES")
        self.assertEqual(references[0].target_paper_id, "s2:ref-1")
        self.assertEqual(citations[0].direction, "CITED_BY")
        self.assertEqual(citations[0].source_paper_id, "s2:cite-1")

    def test_semantic_scholar_depth_two_requires_explicit_opt_in(self):
        adapter = SemanticScholarCitationAdapter(request_json=lambda _: {"data": []})
        with self.assertRaises(ValueError):
            asyncio.run(adapter.references("seed-1", depth=2, run_id="run-1"))

    def test_challenger_failure_is_a_warning_and_not_a_formal_failure(self):
        adapter = ChallengerAdapter(search_fn=lambda _: (_ for _ in ()).throw(RuntimeError("upstream unavailable")))
        result = adapter.search("topic")
        self.assertEqual(result["status"], "DEGRADED")
        self.assertEqual(result["records"], [])
        self.assertIn("upstream unavailable", result["warning"])


if __name__ == "__main__":
    unittest.main()
