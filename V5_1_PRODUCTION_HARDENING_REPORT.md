# 医学科研自动化工作站 v5.1
# Production Hardening & Capability Completion Report

- 生成日期：2026-08-09
- 唯一主工作站基线：`D:\Users\nmls\Documents\CodexProjects\medical-research-workstation`
- 真实 Production Pilot：`D:\Users\nmls\Documents\New project`
- 总体分类：`FAIL=0`；已完成路径为 `PASS`，未完成或需要真实输入/人工决策的路径保留为 `WARN` 或 `BLOCKED`
- 原始数据策略：只读；本阶段没有移动、覆盖、删除或重写 raw data

## 1. 执行边界

本阶段以 v5 已验收的 Windows、WSL2、R、Python、Skills、MCP 和基础工作站为冻结前提，进入 Production Hardening 和 Production Pilot。没有重新搭建或重构已经 PASS 的基础设施，没有为了“覆盖更多能力”自动安装无关新工具，也没有使用 synthetic demo 作为主要科学验收依据。

## 2. 发布、冻结与回滚

| 项目 | 状态 | 证据 |
|---|---|---|
| v5 冻结快照 | PASS | `D:\Users\nmls\Documents\CodexProjects\medical-research-workstation-freeze-v5-20260809` |
| 发布清单 | PASS | `D:\Users\nmls\Documents\CodexProjects\medical-research-workstation-release-v5-accepted-20260809\RELEASE_MANIFEST.json` |
| 冻结校验 | PASS | 261 个文件、581,505 bytes，SHA-256 无差异 |
| v5 接受提交 | PASS | `beb59d7de624dc03942d2f6729fca8355ec08248` |
| v5 接受标签 | PASS | `accepted-v5-20260809` |
| v5.1 控制平面标签 | PASS | `production-hardening-v5.1-20260809` |
| v5.1 观察期报告标签 | PASS | `production-hardening-v5.1-observation-20260809` |
| 远程仓库 / push | PASS | 未配置 remote，未 push |
| 凭据/隐私扫描 | PASS | staged 文件无 secret-pattern 文件命中；凭据值未写入报告 |

已建立本地 Git 的位置只有主工作站根目录。回滚入口为冻结快照、发布清单和 `RESTORE_INSTRUCTIONS.md`；没有执行强制覆盖或破坏性 Git 操作。

## 3. Zotero 与 Obsidian

| 集成 | 状态 | 实际验证 |
|---|---|---|
| Zotero MCP | `WARN` | 只读库发现 PASS；实际连接库报告 190 items |
| Zotero 本地 Desktop/zcli/collection/item 层 | `BLOCKED` | Zotero Desktop 未运行，本地 adapter 为 `not_configured`；未伪造成功，未执行写入 |
| Obsidian 真实 vault | `PASS` | `D:\nmls\Documents\Obsidians\kljk` 存在 `.obsidian`，88 个 Markdown 文件；真实搜索 smoke PASS |
| 项目映射 | `PASS` | `Research Projects/rpl-pci-production-pilot.md`，并登记于 `config/project-integrations.yaml` |

Zotero 当前满足受控的 MCP 只读发现，但不满足本地附件、collection、item DOI/PMID 和 BibTeX 工作流。Obsidian 已完成真实 vault 的只读检查和项目笔记映射。

## 4. 隔离科研运行时

| 运行时 | 状态 | 版本/证据 |
|---|---|---|
| Python scRNA | `PASS` | micromamba env `rpl-pci-scrna`；Python 3.14.6、Scanpy 1.12.3、AnnData 0.13.2、igraph/Leiden smoke PASS |
| R 单细胞 | `PASS` | micromamba env `rpl-pci-r`；R 4.5.3、Seurat 5.5.1、SingleCellExperiment 1.32.0、scDblFinder 1.24.0 smoke PASS |
| 可复现锁定 | `PASS` | `environment/locks/rpl-pci-scrna-linux-64.explicit.txt` 与 `rpl-pci-r-linux-64.explicit.txt` |
| 兼容性记录 | `PASS` | `environment/scRNA-runtime-compatibility-20260809.md` |
| h5py/HDF5 小版本提示 | `WARN` | h5ad 重新打开 PASS；读取时出现非阻断的构建/运行 HDF5 小版本提示，已记录于 CRI |

原有 `bio-base` 环境未被改写。新增运行时只服务于真实 pilot 的 scRNA 生产路径。

## 5. 真实 Production Pilot

### 5.1 项目与数据

- 项目：`D:\Users\nmls\Documents\New project`
- 数据：WEI2022 / GSE214607
- 运行目录：`D:\Users\nmls\Documents\New project\results\scrna-production\run-20260809`
- 输入：16 个真实技术分区，每个分区确定性最多取 1,000 个细胞
- 进入运行的真实细胞：16,000
- 通过核心 QC：15,820
- scDblFinder：16/16 技术分区实际运行并通过
- 结果文件：`filtered_annotated.h5ad`，保留 counts layer、raw、PCA/UMAP 和 QC/双细胞/标签元数据
- 结果清单校验：93/93 文件通过

### 5.2 已跑通的路径

| 阶段 | 状态 | 说明 |
|---|---|---|
| project resolution | PASS | 真实项目及既有控制文件可解析 |
| project.yaml / status.yaml | PASS | 项目配置和状态存在并纳入流程 |
| raw manifest | PASS | 原始输入清单及哈希可回溯 |
| privacy classification | PASS | 未输出凭据值；隐私分级存在 |
| data QC | PASS | 按 library 的观测分布计算阈值；保留原始矩阵 |
| scDblFinder | PASS | 每个技术分区使用真实 scDblFinder；没有静默替代 caller |
| normalization / PCA | PASS | Scanpy normalize/log1p、HVG、PCA |
| neighbors / UMAP / Leiden | PASS | Scanpy 邻域、UMAP、Leiden 完成 |
| annotation | PASS | 保守 marker/cluster 标签；未知细胞不强行归类 |
| donor-aware analysis | PASS | donor pseudobulk 与探索性 donor-aware DE |
| figures / tables | PASS | QC、UMAP、元数据、marker、donor 汇总和 DE 表 |
| provenance / reproduce | PASS | `run_metadata.json`、`run_status.json`、result manifest 与 h5ad reopen smoke |
| manuscript QC | BLOCKED | 当前没有 manuscript draft，无法做真实数字一致性核对 |

### 5.3 重要限制

该运行是可复现的真实数据 operational subset，不是全队列发表级 biological inference。全 cohort 未运行；没有把细胞当作独立生物学重复，donor 是推断单位。ambient RNA correction、匹配参考图谱注释和最终发表级效应解释仍需真实输入、资源评估和人工审查。原始数据运行前后保持只读一致。

## 6. 六个核心科研域验收

证据：`DOMAIN_ACCEPTANCE_REPORT.md`、`DOMAIN_ACCEPTANCE_REPORT.json`。

| 领域 | 路由 | fixture/control smoke | 总体 |
|---|---|---|---|
| 临床观察性研究 | PASS | PASS | PASS |
| qPCR | PASS | PASS | PASS |
| 系统综述 / Meta | PASS | PASS | PASS |
| MR / GWAS | PASS | PASS | WARN（等待真实输入） |
| 公共组学 / bulk RNA | PASS | PASS | WARN（等待真实输入） |
| scRNA | PASS | PASS | PASS |

汇总：`PASS=4`、`WARN=2`、`FAIL=0`、`BLOCKED=0`。MR/GWAS 和公共组学的 WARN 是输入门控，不是合成科学结果；没有把路由通过写成分析完成。

## 7. 自然语言 UX 与控制平面

- 12 个自然语言验收提示全部 PASS：新建项目、继续课题、数据检查、qPCR、系统综述、MR、GEO、单细胞、论文检查、投稿准备、复现和项目阻塞盘点。
- 关键 donor 规则已进入 protected core、scRNA domain pack、routing contract 和回归测试：细胞不能增加生物学重复数，禁止 `unit=cell` 作为推断单位。
- `researchctl doctor`、skills audit、全量 unit test（11/11）和 `optimize --check` 已验证；优化策略为 review-only、自动变更数为 0。

路由验收只证明“选择了正确工作流和门控”，不证明没有输入时已经完成科学分析。

## 8. Submission preflight

报告：`D:\Users\nmls\Documents\New project\reports\SUBMISSION_PREFLIGHT_REPORT.md`。

总体：`BLOCKED`。

- PASS：项目/状态、raw manifest/hash、隐私检查、当前官方网页证据可回读。
- WARN：图表完整性、引用标识、报告规范选择仍需稿件上下文。
- BLOCKED：没有 manuscript source；数字一致性无法完成；目标期刊和具体投稿版本尚未确定。
- 已记录动态核验来源：STROBE、PRISMA 2020、MIQE 以及 Nature 作者/投稿/伦理要求。提交前必须重新核对当前版本，而不是依赖冻结快照。

## 9. C/D CodexProjects 差异审计

证据：

- `C:\Users\nmls\Documents\Codex\2026-08-09\zhe\outputs\c-d-codexprojects-reconciliation-report.md`
- `C:\Users\nmls\Documents\Codex\2026-08-09\zhe\outputs\c-d-codexprojects-file-inventory.csv`
- `C:\Users\nmls\Documents\Codex\2026-08-09\zhe\outputs\c-d-codexprojects-followup-audit.md`

| 项目 | C 盘 | D 盘 |
|---|---:|---:|
| 文件数 | 15,297 | 69,431 |
| 总字节 | 1,421,370,427 | 4,858,478,650 |
| common paths | 15,297 | 15,297 |
| common equal hashes | 15,294 | — |
| common differing | 3 | — |
| D-only | 54,134 | — |

另有 54 个文件级异常行和 2 个枚举异常，复核时 54 个路径均可直接找到，但其中存在特殊 Unicode 路径和树不稳定风险。3 个差异集中在 `Auto-Research-Skills/scienceclaw` 的安全文件实现/测试；C 盘有空文件，D 盘有非空实现，不能自动选择一方覆盖另一方。

结论：`BLOCKED_PENDING_HUMAN_REVIEW`。D 盘仍是目标 canonical root；没有删除、移动、覆盖、junction、批量复制或强行切换兼容入口。

## 10. CRI telemetry 与 observation mode

记录位置：

- `D:\Users\nmls\Documents\New project\logs\cri\production-pilot-telemetry.jsonl`
- `D:\Users\nmls\Documents\New project\logs\cri\observation-mode.yaml`

已记录真实执行中的失败和修正，包括宿主超时、路径修正、缓存复用、重复哈希审计、上下文/工具绕路、submission BLOCKED 和 C/D BLOCKED。没有把这些过程隐藏成单次理想流程。

Observation window 为 2–4 周：允许 weekly housekeeping 和 monthly retrospective；禁止自动修改 Protected Core、自动 promote E2/E3、为了优化而新增工具、raw data 移动/覆盖以及 C/D cutover。

## 11. 最终分类

### PASS

- v5 冻结、发布清单、本地 Git、回滚标签和 secret/privacy gate
- Obsidian 真实 vault 只读 smoke 与项目映射
- Python/R 隔离 scRNA runtime、smoke 和 explicit locks
- 真实 scRNA 16,000-cell operational subset、scDblFinder、Scanpy、donor-aware 输出、provenance 和 reproduction
- 临床、qPCR、系统综述 scaffold、scRNA 四个域的控制验收
- 12/12 自然语言 UX、11/11 unit tests、doctor、skills audit、review-only optimize gate
- observation policy 已落盘

### WARN

- Zotero 当前是 `DEGRADED_LOCAL / MCP_AVAILABLE`，本地 Desktop/zcli/item/attachment 层未配置
- scRNA 是真实 operational subset，不是全 cohort 发表级推断
- h5py/HDF5 构建与运行小版本提示未阻断读取，但应在后续运行时维护中观察
- ambient RNA、参考图谱注释和全量资源评估尚未完成
- MR/GWAS 和公共组学等待真实输入
- submission preflight 的图表、引用标识、报告规范需随 manuscript 和目标期刊确定
- C/D 审计中的异常路径需要后续人工复核

### FAIL

- 当前没有发现已验证的 FAIL 项

### BLOCKED

- 没有 manuscript draft，因此 manuscript QC、数字一致性和最终投稿 preflight 不能完成
- Zotero 本地 collection/item/attachment/BibTeX 工作流未配置
- C/D canonical junction/cutover 仍需人工审查
- 全队列 scRNA 发表级推断未执行
- MR/GWAS、公共组学真实项目分析尚未有实际输入

## 12. 应继续优化的内容

1. 准备真实 manuscript draft，明确目标期刊后重新运行 submission preflight、数字交叉核对和报告规范检查。
2. 在资源和授权明确后决定是否运行 scRNA 全 cohort；保持 donor-level inference、raw read-only 和可复现锁定。
3. 只有日常工作确实需要时，才配置 Zotero Desktop/local adapter/zcli 的本地只读路径。
4. 为 MR/GWAS 和公共组学接入真实输入后再执行实际分析，不用 synthetic result 填充验收。
5. 由人工审查 C/D 三个内容差异、异常路径、备份和兼容入口策略，再决定是否建立 junction 或清理旧树。

## 13. 已经足够、观察期不要再动

1. 不重构已 PASS 的 Windows/WSL2/R/Python/Skills/MCP 基线。
2. 不改写 raw data、既有 metadata、manifest、provenance 和 donor 统计单位规则。
3. 不为增加覆盖率而安装新的无关工具或自动晋级 Protected Core/E2/E3 变更。
4. 不把路由 PASS、fixture PASS 或 operational subset PASS 扩大为完整科研结论。
5. 不在 C/D 审计完成前删除、覆盖、移动或建立 junction。

## 14. 交付索引

- 本报告：`V5_1_PRODUCTION_HARDENING_REPORT.md`
- Pilot 总报告：`D:\Users\nmls\Documents\New project\PRODUCTION_PILOT_REPORT.md`
- scRNA 结果：`D:\Users\nmls\Documents\New project\results\scrna-production\run-20260809`
- Submission preflight：`D:\Users\nmls\Documents\New project\reports\SUBMISSION_PREFLIGHT_REPORT.md`
- 六域验收：`DOMAIN_ACCEPTANCE_REPORT.md`
- 自然语言验收：`NATURAL_LANGUAGE_UX_REPORT.md`
- C/D follow-up：`C:\Users\nmls\Documents\Codex\2026-08-09\zhe\outputs\c-d-codexprojects-followup-audit.md`
