import json
import unittest
from pathlib import Path


FIXTURES = Path(__file__).resolve().parents[2] / "fixtures" / "contracts"


class ProviderContractTests(unittest.TestCase):
    def test_contract_fixtures_have_explicit_fixture_marker_and_expected_envelopes(self):
        expected = {
            "pubmed.json": "records",
            "paper_search.json": "records",
            "clinicaltrials.json": "studies",
            "semantic_scholar.json": "data",
            "doi_verifier.json": "provider_records",
            "challenger.json": "records",
        }
        for filename, key in expected.items():
            payload = json.loads((FIXTURES / filename).read_text(encoding="utf-8"))
            self.assertTrue(payload["fixture"])
            self.assertIn(key, payload)


if __name__ == "__main__":
    unittest.main()
