# Baseline Import Report

## Conclusion

v5 的基线重建已完成。已有 C:\AI-Workstation 和全局能力索引被确认存在，
本项目只承载医学科研差异层，不替换原有 Windows/WSL 基础层，也不复制全局
Skill/MCP/CLI 数据库。

## Imported references

| Source | Role | Observed state |
|---|---|---|
| C:\AI-Workstation | existing AI/dev workstation | present |
| C:\AI-Workstation\bin\doctor.ps1 | existing health check | present; live run completed |
| C:\AI-Workstation\bin\wsl-run.ps1 | Windows to WSL bridge | present; live bridge checks failed because WSL is unusable |
| C:\AI-Workstation\setup\reports\FINAL-REPORT.md | historical baseline report | present; claims a healthier WSL state than the live check |
| C:\Users\nmls\Documents\Codex\2026-08-09\zhe\outputs\tooling-capability-index.md | global capability source of truth | present; 246 Skills, 355 MCP tools, 101 CLI-Hub entries |
| D:\Users\nmls\Documents\CodexProjects\medical-research-workstation | research delta project | present; scaffold existed before v5 reconstruction |

## Import rules applied

- Existing configuration and helper scripts were preserved.
- No software, package, reference data, plugin, or MCP server was installed.
- No old project was modified.
- v3 was not deleted, but was marked historical and superseded.
- Only a research-specific derived capability view is added to this project.
- Secrets and credentials were not copied into reports.

## Baseline conflict

The historical final report says WSL2, Linux doctor, Docker, Jupyter, and the
bio-base layer passed. The 2026-08-09 live doctor run instead reported the
distribution as stopped/unusable and emitted HYPERV_NOT_INSTALLED. Therefore
the historical report is retained as provenance but does not override the live
health result.
