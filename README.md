# Medical Research Workstation

> AI-assisted, auditable and reproducible biomedical research workstation framework.

**Public candidate:** `v1.0.0-rc1` · **Internal baseline:** `v5.1` · **License:** MIT

## English

Medical Research Workstation is a small, deterministic control plane for biomedical research workflows. It connects project metadata, task routing, validated Skills/CLI/MCP boundaries, quality checks, provenance and reproduction records without pretending to replace scientific judgment.

It is designed for clinical observational research, qPCR, systematic reviews/meta-analysis, MR/GWAS planning, public omics, scRNA-seq QC and manuscript/submission gates. The repository contains generic code, schemas, domain contracts and synthetic fixtures only.

### What it is

- A project and status control plane built around `project.yaml` and `status.yaml`.
- A thin `researchctl` CLI for project creation, routing, QC, provenance, reproduction and review gates.
- A Shared Research Core for privacy, statistical-unit, QC and evidence rules.
- A stage-gated medical-manuscript lifecycle controller with separate evidence, author-decision and submission ledgers.
- Platform adapters for Codex and Claude Code that reuse the same research contracts.
- A public-release-safe synthetic smoke workflow and audit tooling.

### What it is not

- Not a medical device, diagnostic system or clinical decision-maker.
- Not an automatic paper-publication or result-generation system.
- Not a substitute for researchers, statisticians, clinicians, ethics review or journal instructions.
- Not a container for patient data, private notes, Zotero attachments, credentials or unpublished manuscripts.

### Quick start

Requirements: Python 3.10+ and Git. Quarto, R, WSL2, external MCP servers and database Skills are optional and must be checked separately.

```bash
python scripts/researchctl.py doctor --json
python scripts/researchctl.py skills audit --json
python scripts/researchctl.py projects --json
python scripts/public_release_audit.py --json
python examples/synthetic/run_synthetic_smoke.py
```

On Windows, the equivalent wrapper is `bin/researchctl.cmd`. Set `RESEARCHCTL_ROOT` when running the control plane from another checkout; do not hard-code a personal workstation path.

### Safety defaults

- Raw data is immutable by default and is never included in public fixtures.
- PHI/PII, secrets, private paths and restricted data are blocked from release artifacts.
- Technical replicates are not biological replicates; cell-level observations do not automatically become donor-level replicates.
- Correlation is not silently promoted to causation.
- High-risk analysis and final submission remain human-gated.
- The public CI does not download large sequencing data or upload research outputs.

### Repository map

| Area | Purpose |
|---|---|
| `scripts/` | Deterministic Python control-plane and release-audit entry points |
| `config/` | Portable policy and example configuration |
| `domain-packs/` | Domain-level routing contracts and safety boundaries |
| `skills/shared/` | Single source of truth for research and release rules |
| `skills/codex/` | Codex adapter |
| `skills/claude/` | Claude Code adapter |
| `skills/medical-manuscript-pipeline/` | End-to-end manuscript gates, logic, author voice, study branches and reusable templates |
| `templates/` | Generic project scaffolds |
| `tests/fixtures/synthetic/` | Small synthetic inputs only |
| `docs/` | Architecture, installation, safety, contribution and release documentation |

See [docs/installation/QUICKSTART.md](docs/installation/QUICKSTART.md), [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) and [docs/release/PUBLIC_RELEASE_READINESS_REPORT.md](docs/release/PUBLIC_RELEASE_READINESS_REPORT.md).

## 中文说明

医学科研自动化工作站是一个轻量、确定性、可审计、可复现的生物医学科研工作流控制层。它把项目元数据、任务路由、已验证的 Skill/CLI/MCP 边界、数据质控、provenance 和 reproduce 连接起来，但不替代科研判断。

适用方向包括临床观察性研究、qPCR、系统综述/Meta、MR/GWAS 方案、公共组学、scRNA-seq 质控以及论文/投稿闸门。公开仓库只包含通用代码、schema、领域契约和 synthetic fixtures，不包含真实科研数据。

### 它能做什么

- 以 `project.yaml` 和 `status.yaml` 管理项目与阶段。
- 通过 `researchctl` 执行项目创建、任务路由、QC、provenance、复现和 review gate。
- 通过 Shared Research Core 统一隐私、统计单位、QC 和证据规则。
- 通过医学论文生命周期控制器管理阶段门控、证据账、作者决定账、投稿准备账、全文逻辑和科学冻结后的去AI。
- 为 Codex 和 Claude Code 提供薄适配器，共享同一套科研约束。
- 提供不接触真实研究数据的 synthetic smoke 和公开发布审计工具。

### 它不能替代什么

- 不是医疗器械、诊断系统或临床决策工具。
- 不是自动发表论文或自动生成科研结论的系统。
- 不能替代研究者、统计师、临床医生、伦理审查或期刊要求。
- 不应放入患者数据、私人笔记、Zotero 附件、凭据或未发表稿件。

### 快速开始

需要 Python 3.10+ 和 Git。Quarto、R、WSL2、外部 MCP 服务和数据库 Skill 都是可选能力，必须单独检查。

```bash
python scripts/researchctl.py doctor --json
python scripts/researchctl.py skills audit --json
python scripts/researchctl.py projects --json
python scripts/public_release_audit.py --json
python examples/synthetic/run_synthetic_smoke.py
```

Windows 用户可以使用 `bin/researchctl.cmd`。如果从其他目录运行，可设置 `RESEARCHCTL_ROOT`；不要把个人电脑路径写死到项目中。

### 安全默认值

- raw data 默认不可变，公开 fixtures 只使用 synthetic data。
- PHI/PII、凭据、私人路径和受限数据禁止进入发布包。
- technical replicate 不等于 biological replicate；细胞级观察不能自动增加 donor 级生物学重复数。
- 不把相关性静默写成因果关系。
- 高风险分析和最终投稿保留人工闸门。
- 公开 CI 不下载大型测序数据，也不上载科研结果。

### 贡献与许可

请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)、[SECURITY.md](SECURITY.md)、[DISCLAIMER.md](DISCLAIMER.md) 和 [docs/release/RELEASE_NOTES.md](docs/release/RELEASE_NOTES.md)。本项目采用 MIT License；使用者需自行负责数据、代码、统计方法、伦理合规和最终结论。
