---
name: literature-search-strategy
description: Build and QA a reproducible database-specific search strategy.
---

# Call when

Call before a formal review or when a question needs PICO, PECO, PCC, SPIDER,
PIRD, or PICOTS concept blocks and database-specific query artifacts.

# Do not call when

Do not call for an informal one-off lookup with no reproducibility requirement.

# Required outputs

Write `runs/<run_id>/search_strategy.yaml`, preserve each database query, and
run query lint plus mandatory known-item recall before locking.
