# Troubleshooting

| Symptom | First check | Safe response |
|---|---|---|
| missing tool | `docs/RUNTIME.md` checks | report blocked prerequisite; do not install implicitly |
| raw mismatch | manifest and SHA-256 | quarantine new ingest; never overwrite |
| unresolved citation | source/status field | mark `VERIFY_REQUIRED`; do not cite formally |
| unit mismatch | protocol/project.yaml | stop analysis and amend protocol explicitly |
| failed external write | service state/read-back | preserve logs; retry only after scope check |
| restricted-data risk | privacy classification and paths | stop upload/logging and redact outputs |
