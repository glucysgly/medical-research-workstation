# Natural-language UX acceptance

| Prompt | Expected workflow | Actual workflow | Primary skill | Status |
|---|---|---|---|---|
| 新建一个临床研究项目 | clinical-observational | clinical-observational | nature-academic-search | PASS |
| 继续这个课题 | project-resume-status | project-resume-status | research | PASS |
| 检查这份数据 | structured | structured | data-analytics:validate-data | PASS |
| 分析这批 qPCR | qpcr | qpcr | data-analytics:validate-data | PASS |
| 做系统综述 | systematic | systematic | nature-academic-search | PASS |
| 做 MR | mr-gwas | mr-gwas | research | PASS |
| 分析这个 GEO | public-omics | public-omics | ngs-analysis:ngs-analysis-router | PASS |
| 做单细胞分析 | scrna | scrna | ngs-analysis:scrna-seq-qc | PASS |
| 检查论文 | manuscript | manuscript | nature-reviewer | PASS |
| 准备投稿 | manuscript | manuscript | nature-reviewer | PASS |
| 复现上次分析 | reproduc | reproduc | superpowers:verification-before-completion | PASS |
| 看看所有项目现在卡在哪里 | project-resume-status | project-resume-status | research | PASS |

Summary: `{'PASS': 12, 'FAIL': 0}`

Routing only selects the workflow and gate; it does not claim that a scientific analysis ran.
