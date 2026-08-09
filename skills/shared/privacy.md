# Shared privacy contract

- Keep raw and restricted data outside public fixtures and release packages.
- Treat unknown data as restricted until classified.
- Do not print or store secrets, private paths, patient identifiers or private
  notes in logs, reports, JSON, CSV or provenance.
- Use counts, redacted paths and statuses when reporting an audit match.
- Require an explicit human gate before upload, publication or external API
  transmission of restricted material.
