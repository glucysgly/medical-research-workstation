# Obsidian integration

Keep project notes in an approved vault with stable relative links to protocol,
literature, results, and retrospective. Restricted content remains local and
must not be synchronized to unapproved services. Use frontmatter for project ID,
status, evidence class, and run ID; check links after edits.

Local adapter: scripts/obsidian_adapter.py. Use health --vault and
search QUERY --vault VAULT [--path SUBDIR]. It is read-only, returns relative
paths and matched lines, rejects path traversal, and does not restructure the
vault.
