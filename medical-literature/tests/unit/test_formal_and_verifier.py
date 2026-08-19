import asyncio
import sys
import unittest
from pathlib import Path


SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))

from medlit.adapters.search.pubmed import PubMedEutilsAdapter  # noqa: E402
from medlit.adapters.verification.doi_fallback import FallbackCitationVerifier  # noqa: E402


class FormalAndVerifierTests(unittest.TestCase):
    def test_pubmed_fallback_normalizes_esearch_and_esummary(self):
        def request_json(url):
            if "esearch.fcgi" in url:
                return {"esearchresult": {"idlist": ["12345"]}}
            return {"result": {"uids": ["12345"], "12345": {"uid": "12345", "title": "PubMed paper", "pubdate": "2024", "fulljournalname": "Journal", "articleids": [{"idtype": "doi", "value": "10.1000/pubmed"}]}}}

        adapter = PubMedEutilsAdapter(email="research@example.org", request_json=request_json)
        papers = asyncio.run(adapter.search("pubmed paper", run_id="run-1"))
        self.assertEqual(papers[0].pmid, "12345")
        self.assertEqual(papers[0].doi, "10.1000/pubmed")
        self.assertEqual(papers[0].source_roles, ["FORMAL_DATABASE"])

    def test_pubmed_fallback_passes_optional_api_key_to_both_entrez_calls(self):
        urls = []

        def request_json(url):
            urls.append(url)
            if "esearch.fcgi" in url:
                return {"esearchresult": {"idlist": ["12345"]}}
            return {"result": {"uids": ["12345"], "12345": {"uid": "12345", "title": "PubMed paper", "pubdate": "2024"}}}

        adapter = PubMedEutilsAdapter(email="research@example.org", api_key="test-key", request_json=request_json)
        asyncio.run(adapter.search("pubmed paper", run_id="run-1"))
        self.assertEqual(len(urls), 2)
        self.assertTrue(all("api_key=test-key" in url for url in urls))

    def test_fallback_verifier_uses_crossref_and_pubmed_metadata(self):
        def lookup(provider, query):
            return {"doi": "10.1000/abc", "title": "A controlled trial", "year": 2024, "authors": ["A. Author"]}

        verifier = FallbackCitationVerifier(lookup=lookup)
        result = asyncio.run(verifier.verify_citation("A controlled trial", "10.1000/abc", None, ["A. Author"], 2024))
        self.assertEqual(result.state, "VERIFIED_HIGH")


if __name__ == "__main__":
    unittest.main()
