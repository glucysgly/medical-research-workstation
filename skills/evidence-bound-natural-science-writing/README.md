# Evidence-Bound Natural-Science Manuscript Revision

## 中文说明

这是一个面向自然科学论文的证据约束型修订 Skill。它借鉴了
[Evidence-Bound Press-Conference Revision Skill](https://github.com/lensback940701/Evidence-Bound-Press-Conference-Revision-Skill)
“提高贡献可见性、但不提高证据允许的主张上限”的核心思想，并将其扩展到
临床研究、实验生物学、qPCR、组学、计算生物学、动物模型和定量研究。

它与 `avoid-overkill` 采用两层组合：

- `avoid-overkill`：冻结用户目标和最小修改范围，阻止无谓扩写、猜测性补充和范围蔓延；
- `evidence-bound-natural-science-writing`：审计研究设计、统计单位、测量层级、效应量与不确定性、引用/图表角色、阴性或矛盾证据，以及修改后的 claim-delta。

自然科学论文的默认流程是：比例控制合同 → evidence contract → 只读审计 → 明确授权 → 最小必要修改 → 整篇科学回归 → stop check。

它不会把横断面关联写成因果，把 mRNA 写成蛋白，把体外扰动写成机制已证实，把内部一致性写成外部验证，也不会通过删除阴性结果、矛盾数据或限制性信息来制造“更强”的结论。

### 适用范围

适合已经有明确研究设计和结果、但存在防御性写作、预写审稿意见、重复限制、埋藏贡献、证据层级混用或验证表述升级的自然科学稿件。

不用于首次起草、新分析、数据质控、文献检索、引文发现、普通语法润色、去 AI 味，或修改研究方法、结局、统计单位、纳入规则和伦理信息。

### 主要交付物

- 诊断：proportionality contract、evidence contract、candidate register、`KEEP/QUERY` 清单、章节集中图和修改建议；
- 授权修订：跟踪版/清洁版、修改摘要、claim-delta 表、统计/图表/引用回归报告、刻意不改项和剩余阻断项。

本 Skill 不替代作者、统计学家、领域专家、期刊报告规范或原始数据核查。未经作者实质性审阅和核验，不应直接提交 AI 改写的论文。

## English description

This Skill provides evidence-bound revision for natural-science manuscripts. It adapts the core idea of the
[Evidence-Bound Press-Conference Revision Skill](https://github.com/lensback940701/Evidence-Bound-Press-Conference-Revision-Skill)
—make the supported contribution easier to see without raising the claim ceiling—to clinical, laboratory, qPCR, omics, computational, animal-model, epidemiological, and quantitative research.

It composes with `avoid-overkill` in two distinct layers:

- `avoid-overkill` freezes the user goal and minimum sufficient scope, preventing speculative additions and scope creep;
- `evidence-bound-natural-science-writing` audits study design, statistical unit, measurement level, effect size and uncertainty, citation/figure roles, negative or discordant evidence, and post-edit claim deltas.

The default workflow is: proportionality contract → evidence contract → read-only audit → explicit authorization → smallest coherent revision → whole-manuscript scientific regression → stop check.

The Skill does not convert cross-sectional association into causation, mRNA into protein, an in-vitro perturbation into a proven mechanism, or internal concordance into external validation. It does not manufacture stronger conclusions by deleting negative findings, discordant datasets, or load-bearing limitations.

### Scope

Use it for a finished or near-finished natural-science manuscript with a defined design and results when defensive prose, reviewer prebuttal, repeated caveats, buried contributions, evidence-level conflation, or inflated validation language obstructs interpretation.

Do not use it for first drafting, new analysis, data QC, literature or citation discovery, generic grammar polishing, Humanizer requests, or changes to methods, outcomes, statistical units, inclusion rules, or ethics.

### Deliverables

- Diagnostic: proportionality contract, evidence contract, candidate register, visible `KEEP/QUERY` decisions, section map, and bounded revision recommendation;
- Authorized revision: tracked/clean manuscript files when supported, change summary, claim-delta table, statistics/figure/citation regression report, deliberate non-edits, and residual blockers.

The Skill does not replace authors, statisticians, domain experts, reporting guidelines, or raw-data verification. AI-assisted revisions require substantive human review before submission.
