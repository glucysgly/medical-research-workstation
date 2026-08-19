# ADR-003: citation provider

## Decision

Use a thin Semantic Scholar Academic Graph adapter for references, citations,
and related papers. Keep depth 1 as the default and preserve graph edges.

## Consequence

Snowballing is auditable and bounded; OpenAlex remains a cross-check rather
than a duplicate top-level search route.
