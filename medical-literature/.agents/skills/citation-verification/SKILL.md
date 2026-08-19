---
name: citation-verification
description: Verify citations before evidence tables or manuscript bibliographies.
---

# Call when

Call after deduplication and before evidence extraction or manuscript use.

# Do not call when

Do not allow a single third-party verifier to become the final truth, and do
not silently convert metadata conflict into a valid citation.

# Policy

Prefer DOI resolver plus authoritative Crossref/PubMed/publisher agreement.
Keep `VERIFIED_HIGH`, `VERIFIED_MEDIUM`, `CONFLICT`, `UNVERIFIED`, and
`INVALID` visible.
