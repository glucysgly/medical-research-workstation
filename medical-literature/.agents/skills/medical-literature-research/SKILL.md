---
name: medical-literature-research
description: Route medical literature tasks into the smallest MLRO V2 workflow.
---

# Call when

Call for medical literature search, evidence collection, trial landscape,
citation tracing, or library-analysis requests.

# Do not call when

Do not call for raw omics analysis, manuscript-only editing, or a single fact
that does not require a literature workflow.

# Boundary

This wrapper identifies the mode, checks capability status, and aggregates
outputs. It must not implement database APIs directly.
