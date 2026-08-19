# V2 citation tracing validation

Status: `READY_FALLBACK`; live network smoke: `PASS`.

Unit coverage confirms backward references produce `CITES` edges, forward
citations produce `CITED_BY` edges, related papers produce `RELATED` edges, and
depth greater than one is blocked without explicit opt-in. Every edge carries
provider, depth, run ID, and deterministic ID.

Read-only smoke on 2026-08-19: the Semantic Scholar API tutorial paper ID
returned 26 `CITES` edges at depth 1. No API key was written or emitted.
