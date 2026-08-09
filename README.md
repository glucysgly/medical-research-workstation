# Codex 医学科研自动化工作站

这是一个以 Codex Desktop 为自然语言入口、以确定性 CLI/API/R/Python/Quarto 为执行层、以项目状态和 provenance 为事实链的个人医学科研工作站。当前唯一执行基线是 v5；v3 已废弃，仅作历史记录。

当前实现重点：

- 先导入并核验已有 Windows/WSL AI 工作站和全局 Skill/MCP/CLI 能力索引，只建设科研差异层。
- 薄 Router：根据意图选择项目、主 Skill、辅助能力和风险门。
- researchctl：项目、状态、审计、QC、路由、provenance、复现和 CRI 的小型标准库 CLI。
- 项目模板：临床观察性研究、qPCR、系统综述/Meta、MR/GWAS、公共组学、探索性分析。
- 科研安全：raw data 不可变、PHI/PII/secret 检查、来源和引用完整性、人工决策闸门。
- 证据链：project.yaml、status.yaml、数据 manifest、分析计划、结果 manifest、provenance。
- CRI：housekeeping、review、feedback、proposal、eval 和 rollback；默认 review-first，不自我修改科研方法。

## 状态

当前已完成 v5 Phase -1 基线重建、WSL2 修复验收和科研差异层核心实现；Windows 基础层、WSL2 桥接、Linux doctor、bio-base、R/Bioconductor 均已通过现场检查。Zotero Desktop、Obsidian 和具体项目数据的可用性仍必须以现场结果为准；本项目不会默认下载大型原始数据或参考数据。

先阅读：

- BASELINE_IMPORT_REPORT.md
- BASELINE_HEALTH_REPORT.md
- RESEARCH_CAPABILITY_GAP.md
- RESEARCH_WORKSTATION_BUILD_PLAN.md
- registry/RESEARCH_CAPABILITY_VIEW.csv

## 入口

~~~powershell
cd D:\Users\nmls\Documents\CodexProjects\medical-research-workstation
.\bin\researchctl.cmd doctor
.\bin\researchctl.cmd projects
.\bin\researchctl.cmd route "把这批 qPCR 数据做完整 QC 和统计"
~~~

更完整的自然语言入口见 QUICK_START.md。
