# Skill 调用条件与科研工作流位置

本文件是七个新增全局 Skill 在医学科研工作站中的调用边界。它们已安装到
`C:\Users\nmls\.codex\skills`；新任务或重新加载 Skills 后生效。所有 Skill 都是按需能力，
不作为所有科研任务的自动后处理步骤。

## 1. `humanizer`：英文文本去 AI 写作痕迹

调用条件：

- 用户明确要求英文 prose 去 AI 味、去 AI 写作痕迹、humanize 或 de-AI；
- 输入是英文摘要、引言、讨论、项目说明、回复信或其他自然语言文本；
- 科学事实、数字、术语、引文和目标语气已经基本确定，Skill 只做表达层改写；
- 文件模式下只改 prose，保留代码块、frontmatter、数据和链接目标。

不调用：

- 用户只要求学术润色、改研究设计或重写统计结论；这些先走 `nature-writing`、
  `nature-polishing` 或相应研究 Skill；
- 代码、表格、原始数据、参考文献字段或需要新增证据的文本；
- 未明确要求去痕的普通校对。

验证要求：逐项核对事实、数字、姓名、技术标识符、引文和科学含义；完成稿件后仍需走
`manuscript-qc` 或人工稿件核查。不要把它当作 AI 检测器，也不要声称改写后一定无法检测。

## 2. `humanizer-zh`：中文文本去 AI 写作痕迹

调用条件：

- 用户明确要求中文去 AI 味、中文去痕、中文人性化或中文自然改写；
- 输入是中文摘要、结果叙述、讨论、科研项目说明、审稿回复或其他自然语言 prose；
- 只处理表达方式、节奏、填充词、宣传式措辞、公式化结构和模糊归因，保留原有事实和证据。

不调用：

- 只需要科学内容改写、证据检索、统计解释或引用补充；
- 代码、数据、参考文献列表、YAML/frontmatter 或需要凭空补充具体数字的文本；
- 没有明确中文去痕意图的普通中文润色。

验证要求：中文 Skill 的例子可能使用示例细节，但科研工作站规则更严格，绝不新增样本量、
时间、结果、机制、引用或临床结论；改写后核对数字、术语、引用位置和结论强度。
中文和英文 Humanizer 按主要语言二选一，默认不串联两次。

## 3. `design-taste-frontend`：研究网站的反模板视觉能力

调用条件：

- 正在建设或重设计科研项目 landing page、公共研究门户、课题组网站、研究成果展示页或作品集；
- 任务需要视觉方向、版式、字体、色彩、动效、真实图片和反模板文案约束；
- 先完成 brief inference 和一行 Design Read，再按项目选择设计系统、动效强度和视觉密度；
- 重设计时先审计现有品牌、信息架构、SEO、无障碍和分析事件，再决定保留或重构。

不调用：

- 论文正文、摘要或一般文字去 AI 味；
- 数据仪表盘、密集数据表、多步骤表单、管理后台、代码编辑器、原生移动 UI；这些走更具体的
  数据、文档或产品 UI 能力；
- 没有真实图片/品牌资产时，不用 div 拼假截图，不把占位视觉当作完成品。

验证要求：检查 Design Read、三项 dial、单一主题、单一 accent、响应式折叠、WCAG 对比度、
暗色模式、`prefers-reduced-motion`、真实视觉资产、动效理由和最终预览。该 Skill 是设计指导，
不代替浏览器渲染、可访问性测试或实际部署。

## 4. `remove-ai-marks`：授权文件的水印与 provenance 清理

调用条件：

- 用户明确要求检查或清理自己拥有或获授权内容中的不可见 Unicode、AI 元数据、C2PA/Content
  Credentials、EXIF、XMP 或容器元数据；
- 输入为文本、Markdown/HTML、PNG/JPEG/WebP、SVG、PDF、DOCX 或 ODT，或需要目录审计；
- 先检查 `WATERMARKS_SERVICE_URL` 默认服务的 `/health`，再检查 `/capabilities`，只根据服务实际能力
  推荐 PDF 元数据、像素水印或 SynthID 相关操作；
- 默认输出 `*.cleaned.*` 副本，保留原文件和 provenance，不直接覆盖 raw data。

服务与边界：

- 该 Skill 只是 HTTP thin client，本机没有服务时必须停止并报告如何启动服务，不能回退为本地清理；
- Layer A 的 Unicode/容器清理是可报告的确定性操作；Layer B 的统计水印处理依赖改写，必须明确提供
  并报告为 best effort；
- 像素水印、音视频水印、C2PA soft binding、密钥型检测器和训练后门不保证覆盖；
- 不能将结果描述为“证明由人类写作”或“保证不可检测”，也不能用于隐瞒应披露的 AI 使用或学术不端。

验证要求：inspect → clean → 读取服务 report → 解码到新文件 → 需要时再次 inspect，并记录清理层、
删除计数、残留风险和服务能力。受限临床数据、原始数据和未经授权文件不进入该流程。

## 5. `life-science-evidence-review`：生命科学证据型综述

调用条件：

- 用户要求生命科学文献综述、证据综合、研究现状概览、基因/基因家族/通路/生物过程综述、知识空白分析或基于证据的研究路线图；
- 任务需要把检索到的研究按主题进行跨研究比较，而不是逐篇摘要；
- 最好能提供物种和性状或生物学主题；代表基因、通路、研究问题、时间范围、目标期刊和输出语言可选；
- 需要生成可追溯的结构化 Evidence Database，并让后续综述、知识空白、未来研究和质量控制都从该数据库派生。

不调用：

- 单篇论文查询、普通 DOI/PMID 查找或只需要一份来源清单；这些走 `nature-academic-search` 或对应数据库 Skill；
- 只做正式 Meta 分析、PRISMA 筛选或风险偏倚流程的任务；主路由仍为 `systematic-review-meta`，除非用户另外要求生命科学主题综合；
- 原始测序数据、组学矩阵、统计建模或实验数据质控；这些走具体 BIO/DATA Skill；
- 只要求语言润色、去 AI 味或改写已有稿件而不要求重新做证据综合。

执行与验证：

- 严格按已安装 Skill 的 `prompt.md → workflow.md → output.md` 顺序执行，不跳过主题理解、背景扩展、检索、批判性评价、证据提取、综合和最终质控；
- 默认交付十项内容：项目摘要、核心文献库、Evidence Database、批判性综述、知识空白矩阵、未来研究机会、证据评估、研究/引用图景、研究路线图和质量控制报告；输出受限时按 Skill 规定的三阶段顺序分批交付；
- 优先原始研究，核对 DOI 与原始链接，去重，并区分已证实结论、证据支持的解释、推断、假设和推测；证据不足时明确报告限制，不补写事实；
- 每个主要结论必须能回溯到 Evidence Database 中的一篇或多篇文献；工作站可配合 `nature-academic-search` 做实时检索、`nature-citation` 做引用核查，但不把 Skill 的计划性输出当成已完成的检索结果。

## 6. `avoid-overkill`：工程与论文的比例控制

调用条件：

- 用户明确要求“最小修复/最小改动”、不要过度设计、不要过度封装、不要添加静默降级或测试补丁、避免范围蔓延；
- 工程任务中已经观察到无谓抽象、猜测性校验、静默 fallback、测试专用分支或相邻改动，需要回到根因和验收信号；
- 论文或审稿回复中需要围绕最强且有证据支持的贡献组织表达，删除自我削弱、预写审稿人意见、工作日志式叙述和空泛 AI 腔；
- 需要按场景选择一个案例文件时，只读取匹配的 `cases/` 条目，不批量加载案例库。

不调用：

- 普通代码编写或论文润色中没有明确的过度工程/防御性表达问题；
- 需要安全、隐私、数据完整性、迁移、认证、计费、破坏性操作或发表证据的强制检查；
- 为了“少做一点”而隐藏矛盾证据、弱化统计不确定性、跳过真实失败复现、绕过明确验收测试或改动用户尚未授权的范围。

验证要求：工程任务核对根因、差异范围、用户可见行为和与风险匹配的验证，并执行 stop check；论文任务核对主张—证据链、术语、引文、矛盾证据和结论边界。该 Skill 约束比例，不替代 `diagnosing-bugs`、统计质控、`nature-citation` 或安全门禁。

## 7. `recreate-scientific-figure-in-drawio`：科研图可编辑重绘

调用条件：

- 用户提供或引用 AI 生成的 PNG/JPEG/SVG/PDF 科研图，并要求重绘、修改、获得可编辑底稿或 `.drawio` 源文件；
- 图的核心内容可以表达为 draw.io 图元：文字、箭头、面板、容器、图例、节点、配色和布局；
- 需要让用户看到可见画布按步骤生成，并在保存前完成图元检查、对齐、重叠、裁切、箭头方向和语义对应性复核；
- 依赖门禁满足：Codex 插件已启用、Draw.io 桌面版可调用、Node.js 22+ 可用，必要时设置 `DRAWIO_PATH`。

不调用：

- 需要从数值数据重新生成的精确统计图、热图、显微照片、复杂曲线或数据可视化；优先走可复现的 `nature-figure`/数据分析流程；
- 参考图分辨率不足以确认文字或科学关系时；应先标出不确定部分，不凭空补全；
- 只要求导出一张扁平图片，或任务需要系统鼠标/键盘、全屏截图控制；该 Skill 只通过 Draw.io 自身 graph/model API；
- 对照片、热图等无法完全图元化的内容，除非用户接受明确标注的栅格部分；不得静默把整张参考图当作“已重绘”。

执行与验证：

- 正常顺序为 `drawio_live_launch → drawio_live_status(graph_ready=true) → add_shape/add_edge/draw_sequence → screenshot → inspect/update/fit → save_snapshot(.drawio) → drawio_validate → drawio_export`；
- 先建立可编辑图元再保存 `.drawio`，不先生成 XML 再打开；所有标签、箭头、分区和图例尽量保持可编辑；
- 默认交付 `.drawio` 可编辑源文件和非嵌入 PNG 复核图；用户确认后再导出嵌入式 PNG/SVG/PDF/JPG，并报告仍为栅格的局部；
- 以后凡是用户提出“AI 生成科研图重绘/可编辑底稿/Draw.io 科研图”请求，工作站自动选择此路由；普通论文图制作仍先判断是否应由可复现数据绘图承担。

## 8. `evidence-bound-natural-science-writing`：自然科学论文证据边界修订

调用条件：

- 稿件已经有明确研究设计和结果，用户要求减少防御性写作、提高贡献可见性、让论文更主动，或要求在返修后增强表达但不能夸大证据；
- 任务涉及 claim ceiling、证据边界、关联/因果、机制、验证、效应量/不确定性、mRNA/蛋白层级、图表与引用角色、内部/外部验证或不一致数据；
- 能提供最新稿件、研究设计/统计单位、结果表图、作者锁定的方法与明确的修改权限；缺失内容可以标记 `VERIFY_REQUIRED` 或 `QUERY`，不凭空补全。

不调用：

- 从零起草论文、补做分析、数据质控、文献检索/引文发现、事实核查、普通语法润色或用户只要求去 AI 味；
- 需要改变主要结局、纳入排除、统计单位、异常值规则、研究方法、伦理信息或原始数据；
- 证据本身不足而用户希望用更强语气掩盖不足。此时保留阻断项，必要时转到具体的统计、数据、文献或审稿 Skill。

执行与验证：

- 先调用 `avoid-overkill` 冻结用户目标、最小必要修改范围和停止条件，再读 `skills/evidence-bound-natural-science-writing/SKILL.md` 及其 `references/natural-science-guardrails.md`，产出 proportionality contract、evidence contract 和只读 candidate register；诊断不自动授权改稿；
- 审计必须区分研究设计/统计单位、测量层级、效应量与不确定性、阴性或矛盾证据、引用/图表角色和作者待决问题；
- 经明确授权后才修改，并额外交付 claim-delta、统计/图表/引用回归报告、刻意不改项和剩余阻断项；
- 本 Skill 的主要能力是证据约束型修订；`avoid-overkill` 是必需的比例控制支持层，不替代 `nature-writing` 的首次起草、`nature-citation` 的来源核查、`nature-reviewer` 的独立审稿或具体数据分析 Skill。

## 工作站组合规则

1. 稿件先用 `nature-writing`/`nature-polishing` 稳定科学表达，再在用户明确要求时选择一个 Humanizer，
   最后做稿件数字、引用和结果一致性核查。
2. “去 AI 味”是写作风格请求，不等于水印清理。文本表达改写走 Humanizer；元数据、不可见字符或
   C2PA 清理走 `remove-ai-marks`，两者不自动串联。
3. `design-taste-frontend` 只对研究网站和公共网页表面生效，不会改变论文科学内容或数据可视化统计口径。
4. `life-science-evidence-review` 负责证据型综述的结构化综合；它与 Humanizer、`remove-ai-marks` 不自动串联。
5. `avoid-overkill` 是显式比例控制层：工程任务走 `proportional-engineering`，论文任务走 `proportional-academic-writing`，不自动套用到所有任务。
6. `evidence-bound-natural-science-writing` 是自然科学论文的证据边界主路由，`avoid-overkill` 是其比例控制支持层；前者负责结构化 claim/evidence 审计和整篇回归，后者负责范围冻结与 stop check，不与普通论文起草或 Humanizer 自动串联。
7. `recreate-scientific-figure-in-drawio` 负责可编辑科研图重绘；它不替代数据来源、统计绘图或科学含义核验，并与 `nature-figure` 按任务边界组合。
8. 所有八个 Skill 都遵守工作站的 raw data 不可变、来源可追溯、无事实杜撰和人工学术责任规则。

## 路由示例

| 用户意图 | 工作流键 | 主 Skill |
|---|---|---|
| 把中文摘要去掉 AI 味，但不改数字和引用 | `manuscript-humanization-zh` | `humanizer-zh` |
| Humanize this English abstract without changing facts | `manuscript-humanization-en` | `humanizer` |
| 设计科研项目 landing page | `research-web-design` | `design-taste-frontend` |
| 检查 PDF 的 C2PA 和元数据 | `artifact-mark-cleaning` | `remove-ai-marks` |
| 围绕某个基因或通路做生命科学证据综述并分析知识空白 | `life-science-evidence-review` | `life-science-evidence-review` |
| 最小修复 bug，不新增抽象和测试补丁 | `proportional-engineering` | `avoid-overkill` |
| 论文删除自我削弱和预写审稿意见 | `proportional-academic-writing` | `avoid-overkill` |
| 自然科学论文做 claim/evidence 审计并在授权后去防御性写作 | `evidence-bound-natural-science-writing` | `avoid-overkill`; `nature-citation` |
| 将 AI 生成科研图重绘为可编辑底稿 | `scientific-figure-drawio-redraw` | `recreate-scientific-figure-in-drawio` |
