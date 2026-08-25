# ADR-001: separate search source roles

## Decision

Every source record carries a role enum. Formal databases, discovery engines,
trial registries, citation edges, challengers, verifiers, local libraries, and
manual imports are separate workflow inputs.

## Consequence

PRISMA/formal counts remain reproducible and challenger/citation output cannot
silently replace a database search.
