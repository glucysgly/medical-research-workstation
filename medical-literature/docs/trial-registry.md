# Trial registry layer

ClinicalTrials.gov API v2 is the primary fallback because it provides a public
study endpoint and documented pagination. The adapter normalizes NCT ID, title,
status, design, phases, enrollment, conditions, interventions, outcomes,
sponsor, dates, results-posted state, locations, and registry references.

Registry and publication records stay separate. Trial-publication links must
carry link type, source, confidence, and verified state. `INFERRED` is never
automatically confirmed. ISRCTN and WHO ICTRP are optional/experimental and do
not block the core.

Authoritative references:

- https://clinicaltrials.gov/data-about-studies/learn-about-api
- https://clinicaltrials.gov/data-api/about-api/study-data-structure
