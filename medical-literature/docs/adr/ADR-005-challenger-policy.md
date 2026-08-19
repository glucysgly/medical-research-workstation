# ADR-005: challenger policy

## Decision

Use scholar-megasearch only in DEEP_DISCOVERY and FORMAL_REVIEW. Its unique
records are QA candidates, never formal counts.

## Consequence

Optional challenger failure is a warning and does not fail the formal search;
confirmed query gaps create a new strategy run.
