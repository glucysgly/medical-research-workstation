# ADR-006: top-level tool exposure

## Decision

Expose workflow-level wrappers and allowlist only the provider tools required
by each route. Vendor implementations stay behind adapters.

## Consequence

The main agent sees a bounded vocabulary instead of many duplicate search
tools, while raw provider provenance remains available in the ledger.
