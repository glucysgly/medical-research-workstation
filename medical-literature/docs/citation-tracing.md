# Citation tracing

`SemanticScholarCitationAdapter.references` creates `CITES` edges from a seed
to its references. `.citations` creates `CITED_BY` edges from a citing paper to
the seed. `.related` creates `RELATED` edges. Every edge includes provider,
depth, run ID, and a deterministic edge ID.

Depth 1 is the default. Depth >1 requires `allow_deep=True` and an explicit
review decision. A failed Semantic Scholar request should degrade to an
OpenAlex cross-check or a warning; it must not erase the formal corpus.

The adapter is based on the official Semantic Scholar Academic Graph API
contract: https://www.semanticscholar.org/product/api/tutorial
