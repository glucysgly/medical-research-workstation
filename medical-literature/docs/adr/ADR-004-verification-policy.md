# ADR-004: citation verification policy

## Decision

Require DOI resolver identity plus at least two authoritative metadata matches
for `VERIFIED_HIGH`. Treat conflicts and absent evidence explicitly.

## Consequence

An AI-found citation cannot enter the final bibliography solely because one
third-party verifier returned a result.
