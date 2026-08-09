# Contributing

1. Create a focused branch from the public candidate.
2. Use synthetic or clearly redistributable fixtures only.
3. Run the unit tests, synthetic smoke and public release audit.
4. Do not weaken privacy, statistical-unit, provenance or human-gate rules to
   make a test pass.
5. Record external dependencies and licenses in
   `docs/release/third-party-inventory.yaml`.
6. Keep Codex and Claude adapters thin; shared research rules belong in
   `skills/shared/`.
7. Explain any Protected Core change and add a regression test.

Suggested checks:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python examples/synthetic/run_synthetic_smoke.py
python scripts/public_release_audit.py --json
```

Pull requests must not include raw data, patient data, private paths,
credentials, private notes, full-text papers or generated local reports.
