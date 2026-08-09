# QUICK START

工作规则：v5 是唯一现行提示词。每项任务先查
registry/RESEARCH_CAPABILITY_VIEW.csv，再从全局能力索引选择最具体的 Skill/MCP/CLI，
最后执行确定性步骤和质量验证。v3 不再参与路由。

最常用的自然语言任务可以直接交给 Codex：

1. 新建一个临床研究项目。
2. 新建一个 qPCR 项目。
3. 继续最近的项目。
4. 检查所有科研项目现在卡在哪里。
5. 导入这份数据并生成数据 manifest。
6. 检查这份数据的缺失、重复、单位和不可能值。
7. 生成分析计划。
8. 查这个课题最近两年的证据。
9. 做系统综述初筛并保留排除原因。
10. 做 MR 并完成敏感性分析。
11. 分析 GEO/公共组学数据。
12. 检查论文结果数字有没有前后矛盾。
13. 准备投稿版。
14. 准备返修。
15. 做本周科研项目 housekeeping。

对应确定性检查：

~~~powershell
.\bin\researchctl.cmd doctor --json
.\bin\researchctl.cmd skills audit --json
.\bin\researchctl.cmd projects --json
.\bin\researchctl.cmd route "检查论文结果数字有没有前后矛盾" --json
.\bin\researchctl.cmd new --template qpcr-study --id demo-qpcr --title "Synthetic qPCR demo"
.\bin\researchctl.cmd status demo-qpcr --json
.\bin\researchctl.cmd qc demo-qpcr --json
.\bin\researchctl.cmd provenance show demo-qpcr --json
.\bin\researchctl.cmd reproduce <run_id> --json
.\bin\researchctl.cmd review weekly
.\bin\researchctl.cmd review monthly
.\bin\researchctl.cmd optimize --check
~~~

基线与差异诊断：

~~~powershell
.\bin\researchctl.cmd doctor --json
Get-Content .\BASELINE_HEALTH_REPORT.md
Get-Content .\RESEARCH_CAPABILITY_GAP.md
~~~

researchctl 只做确定性编排和安全检查；研究设计、证据综合、临床解释、统计方法裁决和最终学术责任仍由 Codex 与研究者共同完成。
