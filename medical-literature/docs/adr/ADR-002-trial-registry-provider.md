# ADR-002: ClinicalTrials.gov official fallback

## Decision

Use a thin official ClinicalTrials.gov API v2 adapter as the reliable fallback;
keep `mcp-pubmed-evidence` optional until contract and live tests pass.

## Consequence

Trial search can degrade independently from PubMed, and registry provenance is
available without installing a broad overlapping search engine.
