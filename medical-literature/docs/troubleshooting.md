# Troubleshooting

| Symptom | Interpretation | Action |
|---|---|---|
| `AUTH_REQUIRED` | A commercial/API credential is missing | Record the gap; do not claim a search occurred |
| `MANUAL_REQUIRED` | CAPTCHA, CNKI, CENTRAL, or human library action | Pause for the authorized user action |
| `DEGRADED` challenger | Optional recall challenger failed | Keep formal run; record warning and continue |
| `CONFLICT` citation | DOI or metadata points to inconsistent records | Human verification before bibliography |
| query lint `ERROR` | Strategy is not safe to lock | Revise query and create a new run |
| SQLite file locked | A connection or external process still holds the DB | Close readers; use the test's explicit connection lifecycle |

Raw payloads and previous run directories are audit evidence. Do not delete or
rewrite them to make a report pass.
