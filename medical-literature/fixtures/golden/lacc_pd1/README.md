# LACC / PD-1 / PD-L1 public golden-set scope

The public search fixture contains seven mandatory direct-evidence papers in
`fixtures/search/known_items.yaml` and three contextual records. The records
were checked against the supplied review reference list and PubMed metadata;
they are public bibliographic metadata, not private user data.

This fixture establishes identifier and topic scope. A live recall PASS still
requires running a complete database-specific query and recording its run ID,
query, retrieval date, and raw export. The fixture does not by itself prove
formal-review completeness.

Trial-registry records, publication links, citation edges, and challenger
delta review remain separate fixtures because the V2 model intentionally keeps
those source roles distinct.
