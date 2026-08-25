# 医学文献研究编排器 V2（MLRO V2）

这是一个面向医学文献检索、去重、来源追溯和证据工作流的确定性编排模块。英文说明见 [README.md](README.md)。

## 发布状态

`CORE_READY / OPTIONAL_PENDING`

当前发布的是“核心可用、可选能力待授权/待接入”版本。没有商业数据库权限、CNKI 登录或合法导出文件时，系统不会声称已经检索过 Embase、Web of Science、Scopus、CNKI 或 CENTRAL。

## 已包含能力

- QUICK、DEEP_DISCOVERY、FORMAL_REVIEW、SEED_EXPANSION、TRIAL_LANDSCAPE 确定性路由；
- 正式数据库、发现引擎、试验注册库、引文追踪、挑战者、校验器、本地文献库和人工导入的来源角色分离；
- 检索式检查、标准化、保留 provenance 的去重、SQLite 文献台账、试验标准化、引文边、引用校验和召回 QA；
- PubMed E-utilities 与 ClinicalTrials.gov 官方 API 薄适配器；
- 默认深度为 1 的 Semantic Scholar 引文追踪；
- 可选供应商或商业数据库不可用时的明确降级状态；
- 本地全文优先策略，以及 Zotero、MinerU、PaperQA2 的集成接口；
- 离线 E2E fixture、标准库单元测试、契约测试和方法学测试。

## 快速开始

在本目录执行：

```powershell
python scripts/medlit.py doctor --json
python scripts/medlit.py capabilities --json
python scripts/medlit.py route "我要做正式系统综述" --json
python scripts/medlit.py strategy --database pubmed --query '(cervical cancer AND immunotherapy)' --json
python scripts/medlit.py e2e --output-root .\runs\offline-e2e
python -m unittest discover -s tests -p 'test_*.py' -v
```

配置步骤见 [中文配置指南](docs/configuration-guide.zh-CN.md)，英文版见 [English configuration guide](docs/configuration-guide.en-US.md)。

## 科研与安全边界

- 正式数据库计数与 discovery/challenger 计数始终分开；
- 注册试验与已发表论文是两个实体，通过 provenance 关联；
- 引文追踪有深度限制，默认不进行无限递归；
- 商业数据库认证、CNKI 验证码、私人 Zotero PDF 和云端全文上传都必须经过明确授权；
- API key 只放在本地环境或密钥管理器中，不写入仓库；
- 离线测试通过只能证明编排契约有效，不能证明在线综述的科学完整性。

## 通用版限制

当前版本属于 `CORE_READY / OPTIONAL_PENDING`。PubMed/ClinicalTrials.gov fallback、引文追踪、标准化、去重、provenance、搜索 QA 和离线 E2E 已有代码与 fixture；外部 MCP、商业数据库、在线 challenger 比较、规模化试验-论文映射、全文获取、偏倚风险和证据综合仍需单独授权、接入和验证。

详细验收矩阵见 [docs/validation/v2-final-acceptance.md](docs/validation/v2-final-acceptance.md)。
