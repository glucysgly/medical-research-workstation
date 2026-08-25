# Citation verification

The fallback verifier compares DOI, title, year, and author context against
Crossref and PubMed-style authoritative records. `VERIFIED_HIGH` requires an
exact DOI, high title similarity, year consistency, and at least two
authoritative providers. A DOI/title conflict becomes `CONFLICT`; missing
provider evidence remains `UNVERIFIED`.

Only `VERIFIED_HIGH`/`VERIFIED_MEDIUM` records should enter an evidence table
or manuscript bibliography without human confirmation. DOI MCP is an optional
accelerator, not the final truth.
