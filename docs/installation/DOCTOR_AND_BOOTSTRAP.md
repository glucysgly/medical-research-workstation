# Doctor and bootstrap

`researchctl doctor` checks the portable project structure, required local
tools and privacy defaults without printing environment values. It is a
diagnostic command, not an installer.

`scripts/bootstrap.py` performs a bounded setup plan. `--dry-run` is the safe
first step. Normal execution only creates local project/cache/log directories
under the selected root; it does not install packages, modify system settings,
read private Zotero/Obsidian data, upload files or overwrite existing files.

```bash
python scripts/bootstrap.py --dry-run --json
python scripts/bootstrap.py --json
python scripts/researchctl.py doctor --json
```

Platform status is intentionally conservative: the public candidate is tested
with local Python/Git controls; WSL2, R, Quarto, MCP servers and domain-specific
database tools are optional and must be verified in the user's environment.
