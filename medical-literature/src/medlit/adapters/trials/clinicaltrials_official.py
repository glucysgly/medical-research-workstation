from __future__ import annotations

import asyncio
import json
from typing import Any, Callable
from urllib.parse import quote
from urllib.request import Request, urlopen

from medlit.domain.models import ClinicalTrial


def _path(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
    return default if current is None else current


def _values(items: Any, key: str | None = None) -> list[str]:
    output: list[str] = []
    for item in items or []:
        value = item.get(key) if key and isinstance(item, dict) else item
        if value and str(value) not in output:
            output.append(str(value))
    return output


def normalize_trial_record(record: dict[str, Any], *, raw_source: str) -> ClinicalTrial:
    p = record.get("protocolSection", record)
    identification = p.get("identificationModule", {})
    status = p.get("statusModule", {})
    design = p.get("designModule", {})
    conditions = p.get("conditionsModule", {})
    interventions = p.get("armsInterventionsModule", {})
    outcomes = p.get("outcomesModule", {})
    sponsors = p.get("sponsorCollaboratorsModule", {})
    contacts = p.get("contactsLocationsModule", {})
    eligibility = p.get("eligibilityModule", {})
    nct_id = str(identification.get("nctId") or "").upper()
    if not nct_id.startswith("NCT"):
        raise ValueError("ClinicalTrials.gov record is missing a valid NCT identifier")
    return ClinicalTrial(
        trial_id=nct_id,
        registry="ClinicalTrials.gov",
        title=str(identification.get("officialTitle") or identification.get("briefTitle") or "").strip(),
        brief_summary=_path(p, "descriptionModule", "briefSummary"),
        status=status.get("overallStatus"),
        study_type=design.get("studyType"),
        phase=[str(v) for v in design.get("phases", [])],
        enrollment=_path(design, "enrollmentInfo", "count"),
        conditions=_values(conditions.get("conditions")),
        interventions=_values(interventions.get("interventions"), "name"),
        comparators=_values(interventions.get("armGroups"), "label"),
        primary_outcomes=_values(outcomes.get("primaryOutcomes"), "measure"),
        secondary_outcomes=_values(outcomes.get("secondaryOutcomes"), "measure"),
        eligibility=eligibility.get("eligibilityCriteria"),
        sponsor=_path(sponsors, "leadSponsor", "name"),
        collaborators=_values(sponsors.get("collaborators"), "name"),
        locations=_values(contacts.get("locations"), "facility"),
        start_date=_path(status, "startDateStruct", "date"),
        primary_completion_date=_path(status, "primaryCompletionDateStruct", "date"),
        completion_date=_path(status, "completionDateStruct", "date"),
        results_posted=bool(status.get("resultsFirstPostDateStruct")),
        linked_publications=_values(p.get("referencesModule", {}).get("references"), "pmid"),
        raw_source=raw_source,
    )


class OfficialClinicalTrialsAdapter:
    """Thin read-only adapter for the official ClinicalTrials.gov API v2."""

    base_url = "https://clinicaltrials.gov/api/v2"

    def __init__(self, request_json: Callable[[str], dict[str, Any]] | None = None):
        self._request_json = request_json or self._request

    @staticmethod
    def _request(url: str) -> dict[str, Any]:
        request = Request(url, headers={"Accept": "application/json", "User-Agent": "medlit/0.1"})
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

    async def search(self, query: str, *, page_size: int = 100, max_pages: int = 10) -> list[ClinicalTrial]:
        url = f"{self.base_url}/studies?query.term={quote(query)}&pageSize={min(page_size, 1000)}&format=json"
        records: list[ClinicalTrial] = []
        for _ in range(max_pages):
            payload = await asyncio.to_thread(self._request_json, url)
            records.extend(normalize_trial_record(item, raw_source=url) for item in payload.get("studies", []))
            token = payload.get("nextPageToken")
            if not token:
                break
            url = f"{self.base_url}/studies?query.term={quote(query)}&pageSize={min(page_size, 1000)}&pageToken={quote(token)}&format=json"
        return records

    async def get_trial(self, nct_id: str) -> ClinicalTrial:
        clean = nct_id.upper().strip()
        if not clean.startswith("NCT"):
            raise ValueError("nct_id must start with NCT")
        url = f"{self.base_url}/studies/{quote(clean)}"
        payload = await asyncio.to_thread(self._request_json, url)
        return normalize_trial_record(payload, raw_source=url)
