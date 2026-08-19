import asyncio
import sys
import unittest
from pathlib import Path


SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))

from medlit.adapters.trials.clinicaltrials_official import normalize_trial_record  # noqa: E402
from medlit.canonical.normalize import deduplicate_papers, normalize_paper  # noqa: E402
from medlit.domain.models import CitationEdge, SourceRole  # noqa: E402


class DomainTests(unittest.TestCase):
    def test_dedup_merges_identifiers_and_source_provenance(self):
        first = normalize_paper(
            {
                "title": "A controlled trial",
                "doi": "https://doi.org/10.1000/ABC.",
                "authors": [{"name": "A. Author"}],
            },
            source="pubmed",
            source_role=SourceRole.FORMAL_DATABASE,
            run_id="run-formal",
            query="controlled trial",
        )
        second = normalize_paper(
            {
                "title": "A controlled trial",
                "pmid": "12345",
                "keywords": ["trial"],
            },
            source="paper-search",
            source_role=SourceRole.DISCOVERY_ENGINE,
            run_id="run-discovery",
            query="controlled trial",
        )

        merged, audit = deduplicate_papers([first, second])

        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0].doi, "10.1000/abc")
        self.assertEqual(merged[0].pmid, "12345")
        self.assertEqual(set(merged[0].source_roles), {"FORMAL_DATABASE", "DISCOVERY_ENGINE"})
        self.assertEqual(audit[0]["match_rule"], "normalized_title_exact")

    def test_citation_edge_rejects_depth_zero_and_invalid_direction(self):
        with self.assertRaises(ValueError):
            CitationEdge("e1", "p1", "p2", "CITES", "semantic-scholar", 0, "run")
        with self.assertRaises(ValueError):
            CitationEdge("e1", "p1", "p2", "UNKNOWN", "semantic-scholar", 1, "run")

    def test_clinicaltrials_v2_record_normalizes_nct_and_core_fields(self):
        record = {
            "protocolSection": {
                "identificationModule": {
                    "nctId": "NCT01234567",
                    "briefTitle": "A registry trial",
                    "officialTitle": "A registry trial of an intervention",
                },
                "statusModule": {
                    "overallStatus": "RECRUITING",
                    "startDateStruct": {"date": "2025-01-01"},
                    "completionDateStruct": {"date": "2027-01-01"},
                },
                "designModule": {
                    "studyType": "INTERVENTIONAL",
                    "phases": ["PHASE2"],
                    "enrollmentInfo": {"count": 120},
                },
                "conditionsModule": {"conditions": ["Cervical cancer"]},
                "armsInterventionsModule": {
                    "interventions": [{"name": "Intervention X", "type": "DRUG"}]
                },
                "sponsorCollaboratorsModule": {"leadSponsor": {"name": "Sponsor"}},
                "outcomesModule": {
                    "primaryOutcomes": [{"measure": "Overall survival"}],
                    "secondaryOutcomes": [{"measure": "Safety"}],
                },
            }
        }

        trial = normalize_trial_record(record, raw_source="clinicaltrials.gov")

        self.assertEqual(trial.trial_id, "NCT01234567")
        self.assertEqual(trial.status, "RECRUITING")
        self.assertEqual(trial.enrollment, 120)
        self.assertEqual(trial.conditions, ["Cervical cancer"])
        self.assertEqual(trial.primary_outcomes, ["Overall survival"])


if __name__ == "__main__":
    unittest.main()
