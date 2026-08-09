# Security and privacy

## Never commit

- API keys, tokens, passwords, cookies, private keys or credential exports.
- Patient identifiers, PHI/PII, linkage keys or restricted-access data.
- Private Zotero attachments, Obsidian notes, unpublished manuscripts or raw
  sequencing data.
- Machine-specific absolute paths, internal hostnames or connection strings.

Use environment variables or local configuration outside Git. The public
candidate intentionally keeps external uploads blocked and third-party
integrations read-first.

## Reporting a vulnerability

Do not disclose sensitive details in a public issue. Contact the repository
maintainer through the private security channel configured for the repository,
or provide a minimal non-sensitive reproduction in a private channel. Include
impact, affected version, reproduction steps and a proposed mitigation, but
never include real credentials or research data.

## Release checks

Run `python scripts/public_release_audit.py --json` before publishing. A
release must not contain unexplained secret, private-path, PHI/PII or license
matches.
